"""
Call Scheduler Backend
Manages scheduled calls and integrates with Call API at localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import requests
import atexit
import threading
import time

app = Flask(__name__)
CORS(app)

# Configuration
CALL_API_URL = "http://localhost:5000"
DB_PATH = "scheduler.db"

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Shutdown scheduler on exit
atexit.register(lambda: scheduler.shutdown())


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database schema"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS scheduled_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            call_api_id TEXT,
            call_status TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            error_message TEXT
        )
    ''')
    conn.commit()
    conn.close()


def initiate_call_with_api(phone_number):
    """Call the external Call API to initiate a call"""
    try:
        response = requests.post(
            f"{CALL_API_URL}/api/call",
            json={"phone_number": phone_number},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error calling API: {e}")
        return None


def check_scheduled_calls():
    """Background job to check and initiate scheduled calls"""
    conn = get_db()
    now = datetime.now().isoformat()
    
    # Get pending calls that should be made now
    cursor = conn.execute(
        "SELECT * FROM scheduled_calls WHERE status = 'pending' AND scheduled_time <= ?",
        (now,)
    )
    calls = cursor.fetchall()
    
    for call in calls:
        # Initiate the call
        result = initiate_call_with_api(call['phone_number'])
        
        if result and result.get('success'):
            call_data = result.get('call', {})
            # Update status to in-progress
            conn.execute(
                """UPDATE scheduled_calls 
                   SET status = 'in-progress', 
                       call_api_id = ?,
                       call_status = ?,
                       updated_at = ?
                   WHERE id = ?""",
                (call_data.get('id'), call_data.get('status'), datetime.now().isoformat(), call['id'])
            )
        else:
            # Mark as failed
            conn.execute(
                """UPDATE scheduled_calls 
                   SET status = 'failed',
                       error_message = ?,
                       updated_at = ?
                   WHERE id = ?""",
                ("Failed to initiate call", datetime.now().isoformat(), call['id'])
            )
    
    conn.commit()
    conn.close()


def poll_active_calls():
    """Poll Call API for active call statuses"""
    conn = get_db()
    
    # Get all in-progress calls
    cursor = conn.execute(
        "SELECT * FROM scheduled_calls WHERE status = 'in-progress'"
    )
    calls = cursor.fetchall()
    
    for call in calls:
        if not call['call_api_id']:
            continue
            
        try:
            response = requests.get(
                f"{CALL_API_URL}/api/call/{call['call_api_id']}",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('success'):
                call_data = data.get('call', {})
                call_status = call_data.get('status')
                
                # Update call status
                conn.execute(
                    """UPDATE scheduled_calls 
                       SET call_status = ?,
                           updated_at = ?
                       WHERE id = ?""",
                    (call_status, datetime.now().isoformat(), call['id'])
                )
                
                # If call is completed, mark as completed
                if call_status == 'completed':
                    conn.execute(
                        """UPDATE scheduled_calls 
                           SET status = 'completed',
                               updated_at = ?
                           WHERE id = ?""",
                        (datetime.now().isoformat(), call['id'])
                    )
        except Exception as e:
            print(f"Error polling call {call['call_api_id']}: {e}")
    
    conn.commit()
    conn.close()


# Schedule background jobs
scheduler.add_job(check_scheduled_calls, 'interval', seconds=30, id='check_calls')
scheduler.add_job(poll_active_calls, 'interval', seconds=5, id='poll_calls')


@app.route('/api/schedule', methods=['POST'])
def schedule_call():
    """Schedule a new call"""
    data = request.get_json()
    
    if not data or 'phone_number' not in data or 'scheduled_time' not in data:
        return jsonify({'error': 'phone_number and scheduled_time are required'}), 400
    
    phone_number = data['phone_number']
    scheduled_time = data['scheduled_time']
    
    # Validate phone number
    if len(phone_number) < 10:
        return jsonify({'error': 'Invalid phone number'}), 400
    
    # Validate datetime format
    try:
        datetime.fromisoformat(scheduled_time)
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    now = datetime.now().isoformat()
    
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO scheduled_calls 
           (phone_number, scheduled_time, status, created_at, updated_at)
           VALUES (?, ?, 'pending', ?, ?)""",
        (phone_number, scheduled_time, now, now)
    )
    call_id = cursor.lastrowid
    conn.commit()
    
    # Get the created call
    cursor = conn.execute("SELECT * FROM scheduled_calls WHERE id = ?", (call_id,))
    call = dict(cursor.fetchone())
    conn.close()
    
    return jsonify({
        'success': True,
        'call': call
    }), 201


@app.route('/api/calls', methods=['GET'])
def get_calls():
    """Get all scheduled calls"""
    conn = get_db()
    cursor = conn.execute(
        "SELECT * FROM scheduled_calls ORDER BY scheduled_time DESC"
    )
    calls = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'calls': calls
    }), 200


@app.route('/api/calls/<int:call_id>', methods=['GET'])
def get_call(call_id):
    """Get a specific scheduled call"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM scheduled_calls WHERE id = ?", (call_id,))
    call = cursor.fetchone()
    conn.close()
    
    if not call:
        return jsonify({'error': 'Call not found'}), 404
    
    return jsonify({
        'success': True,
        'call': dict(call)
    }), 200


@app.route('/api/calls/<int:call_id>', methods=['DELETE'])
def delete_call(call_id):
    """Delete/cancel a scheduled call"""
    conn = get_db()
    
    # Check if call exists and is pending
    cursor = conn.execute("SELECT * FROM scheduled_calls WHERE id = ?", (call_id,))
    call = cursor.fetchone()
    
    if not call:
        conn.close()
        return jsonify({'error': 'Call not found'}), 404
    
    if call['status'] != 'pending':
        conn.close()
        return jsonify({'error': 'Can only delete pending calls'}), 400
    
    conn.execute("DELETE FROM scheduled_calls WHERE id = ?", (call_id,))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Call deleted'
    }), 200


@app.route('/api/call-now', methods=['POST'])
def call_now():
    """Immediately initiate a call without scheduling"""
    data = request.get_json()
    
    if not data or 'phone_number' not in data:
        return jsonify({'error': 'phone_number is required'}), 400
    
    phone_number = data['phone_number']
    
    # Validate phone number
    if len(phone_number) < 10:
        return jsonify({'error': 'Invalid phone number'}), 400
    
    # Call the external API
    result = initiate_call_with_api(phone_number)
    
    if not result or not result.get('success'):
        return jsonify({'error': 'Failed to initiate call'}), 500
    
    call_data = result.get('call', {})
    now = datetime.now().isoformat()
    
    # Save to database
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO scheduled_calls 
           (phone_number, scheduled_time, status, call_api_id, call_status, created_at, updated_at)
           VALUES (?, ?, 'in-progress', ?, ?, ?, ?)""",
        (phone_number, now, call_data.get('id'), call_data.get('status'), now, now)
    )
    call_id = cursor.lastrowid
    conn.commit()
    
    # Get the created call
    cursor = conn.execute("SELECT * FROM scheduled_calls WHERE id = ?", (call_id,))
    call = dict(cursor.fetchone())
    conn.close()
    
    return jsonify({
        'success': True,
        'call': call
    }), 201


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    init_db()
    print("🚀 Call Scheduler Backend starting on http://localhost:3000")
    print("📞 Connecting to Call API at http://localhost:5000")
    app.run(port=3000, debug=True)
