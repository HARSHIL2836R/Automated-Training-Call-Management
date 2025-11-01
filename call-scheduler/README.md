# Call Scheduler Application

A full-stack call scheduling and management application that integrates with an external Call API.

## 🏗️ Architecture

- **Backend**: Flask REST API with SQLite database and APScheduler
- **Frontend**: HTML/CSS/JavaScript application with real-time updates
- **Integration**: Communicates with Call API at `localhost:5000`

## 📁 Project Structure

```
call-scheduler/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── scheduler.db        # SQLite database (created on first run)
└── frontend/
    └── index.html          # Standalone web application
```

## 🚀 How to Run

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Step 1: Start the Call API (Provided)

```bash
cd interview
pip install -r requirements.txt
python api_server.py
```

The Call API will run on `http://localhost:5000`

### Step 2: Start the Backend

Open a new terminal:

```bash
cd call-scheduler/backend
pip install -r requirements.txt
python app.py
```

The backend will run on `http://localhost:3000`

### Step 3: Open the Frontend

Simply open the HTML file in your browser:

```bash
# Option 1: Double-click the file
call-scheduler/frontend/index.html

# Option 2: Open from command line (Windows)
start call-scheduler/frontend/index.html

# Option 3: Drag the file into your browser
```

The frontend will connect to your backend at `http://localhost:3000`

## ✨ Features

### Core Features

1. **Schedule Calls**: Set a phone number and future datetime to schedule a call
2. **Call Now**: Immediately initiate a call without scheduling
3. **View All Calls**: See all scheduled, in-progress, and completed calls
4. **Real-time Status Updates**: Automatically updates call statuses every 3 seconds
5. **Delete Pending Calls**: Cancel calls that haven't been initiated yet
6. **Filter Calls**: Filter by status (All, Pending, In Progress, Completed)

### Technical Features

- **Automatic Scheduling**: Background job checks every 30 seconds for pending calls
- **Status Polling**: Polls Call API every 5 seconds for active call updates
- **Persistent Storage**: SQLite database stores all call records
- **Error Handling**: Graceful error handling and user feedback
- **Responsive Design**: Works on desktop and mobile devices

## 🎯 API Endpoints

### Backend API (localhost:3000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/schedule` | Schedule a new call |
| POST | `/api/call-now` | Initiate an immediate call |
| GET | `/api/calls` | Get all scheduled calls |
| GET | `/api/calls/:id` | Get a specific call |
| DELETE | `/api/calls/:id` | Delete a pending call |
| GET | `/health` | Health check |

### Request Examples

**Schedule a Call:**
```json
POST /api/schedule
{
  "phone_number": "+1234567890",
  "scheduled_time": "2025-11-01T15:30:00"
}
```

**Call Now:**
```json
POST /api/call-now
{
  "phone_number": "+1234567890"
}
```

## 📊 Database Schema

```sql
CREATE TABLE scheduled_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    scheduled_time TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    call_api_id TEXT,
    call_status TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    error_message TEXT
);
```

## 🔄 Call Status Flow

1. **Pending** → Call is scheduled, waiting for scheduled time
2. **In-Progress** → Call has been initiated with Call API
3. **Completed** → Call has finished successfully
4. **Failed** → Call failed to initiate

### Call API Status (for in-progress calls):
- Initiated → Ringing → Connected → Completed

## 🎨 Design Decisions

### 1. Technology Stack
- **React**: Modern, component-based UI with good developer experience
- **SQLite**: Lightweight, persistent storage without additional setup
- **APScheduler**: Robust Python scheduling library with cron-like features
- **Flask**: Simple, flexible Python web framework

### 2. Architecture Choices
- **Polling Strategy**: 5-second intervals for active calls balance responsiveness with API load
- **Scheduler Frequency**: 30-second checks for pending calls avoid unnecessary CPU usage
- **Frontend Updates**: 3-second refresh keeps UI current without overwhelming the backend

### 3. Trade-offs Made

**Chosen Approach** | **Alternative** | **Reasoning**
--- | --- | ---
SQLite | In-memory dict | Persistence across restarts, more realistic
APScheduler | Simple threading | Better scheduling features, more robust
Polling | WebSockets | Simpler implementation, works with provided API
Server timezone | User timezone | Simpler implementation, reduced complexity
React | Vanilla JS | Better code organization, easier to maintain

## 🧪 Testing the Application

1. **Schedule a future call**:
   - Enter phone number: `+1234567890`
   - Select a time 1-2 minutes in the future
   - Click "Schedule Call"

2. **Test immediate call**:
   - Enter phone number
   - Click "Call Now"
   - Watch status updates in real-time

3. **Monitor progress**:
   - Status changes: Pending → In-Progress → Completed
   - Call status updates: Initiated → Ringing → Connected → Completed

4. **Test filtering**:
   - Use filter buttons to view calls by status

5. **Test deletion**:
   - Delete a pending call (only pending calls can be deleted)

## 🐛 Troubleshooting

**Backend won't start:**
- Ensure Call API is running on port 5000
- Check if port 3000 is available
- Verify Python dependencies are installed

**Frontend won't connect:**
- Verify backend is running on port 3000
- Check browser console for CORS errors
- Ensure CORS is enabled in backend

**Calls not being initiated:**
- Check backend terminal for error logs
- Verify Call API is responding (`curl http://localhost:5000/health`)
- Check database for call records

## 📝 Notes

- All times are in server local timezone
- Database file (`scheduler.db`) is created automatically on first run
- Call status polling only occurs for in-progress calls
- Pending calls can be deleted, but in-progress/completed calls cannot

## 🎓 What I Learned

This assignment demonstrates:
- External API integration patterns
- Background job scheduling
- Real-time status updates
- Database design for scheduling systems
- Full-stack application development
- Time-constrained development decisions

---

**Built in 1 hour for SynCoach Interview Assignment**
