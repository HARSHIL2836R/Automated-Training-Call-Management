"""
Test script to verify the Call Scheduler is working correctly
"""

import requests
import time
from datetime import datetime, timedelta

BACKEND_URL = "http://localhost:3000"
CALL_API_URL = "http://localhost:5000"

def test_health_checks():
    """Test that both servers are running"""
    print("🔍 Testing server health...")
    
    try:
        # Test Call API
        response = requests.get(f"{CALL_API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Call API is running (port 5000)")
        else:
            print("❌ Call API health check failed")
            return False
    except Exception as e:
        print(f"❌ Call API not reachable: {e}")
        return False
    
    try:
        # Test Backend
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running (port 3000)")
        else:
            print("❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"❌ Backend not reachable: {e}")
        return False
    
    return True

def test_immediate_call():
    """Test the call-now functionality"""
    print("\n📞 Testing immediate call...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/call-now",
            json={"phone_number": "+1234567890"},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Call initiated successfully!")
            print(f"   Call ID: {data['call']['id']}")
            print(f"   Status: {data['call']['status']}")
            return data['call']['id']
        else:
            print(f"❌ Failed to initiate call: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_schedule_call():
    """Test scheduling a call"""
    print("\n📅 Testing call scheduling...")
    
    # Schedule a call for 1 minute from now
    scheduled_time = (datetime.now() + timedelta(minutes=1)).isoformat()
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/schedule",
            json={
                "phone_number": "+9876543210",
                "scheduled_time": scheduled_time
            },
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Call scheduled successfully!")
            print(f"   Call ID: {data['call']['id']}")
            print(f"   Scheduled for: {scheduled_time}")
            return data['call']['id']
        else:
            print(f"❌ Failed to schedule call: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_calls():
    """Test retrieving all calls"""
    print("\n📋 Testing get all calls...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/calls", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data['calls'])} calls")
            for call in data['calls'][:3]:  # Show first 3
                print(f"   - {call['phone_number']} | Status: {call['status']}")
            return True
        else:
            print(f"❌ Failed to get calls: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_delete_call(call_id):
    """Test deleting a pending call"""
    print(f"\n🗑️ Testing delete call (ID: {call_id})...")
    
    try:
        response = requests.delete(f"{BACKEND_URL}/api/calls/{call_id}", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Call deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete call: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def monitor_call_progress(call_id, duration=15):
    """Monitor a call's progress for a specified duration"""
    print(f"\n👀 Monitoring call progress for {duration} seconds...")
    
    start_time = time.time()
    last_status = None
    
    while time.time() - start_time < duration:
        try:
            response = requests.get(f"{BACKEND_URL}/api/calls/{call_id}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                call = data['call']
                current_status = f"{call['status']} | {call.get('call_status', 'N/A')}"
                
                if current_status != last_status:
                    print(f"   Status changed: {current_status}")
                    last_status = current_status
            
            time.sleep(2)
        except Exception as e:
            print(f"   Error monitoring: {e}")
            break
    
    print("✅ Monitoring complete")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Call Scheduler Test Suite")
    print("=" * 60)
    
    # Test 1: Health checks
    if not test_health_checks():
        print("\n❌ Servers are not running. Please start them first.")
        print("\nStart order:")
        print("1. python api_server.py")
        print("2. python app.py (in backend folder)")
        return
    
    # Test 2: Get existing calls
    test_get_calls()
    
    # Test 3: Immediate call
    call_id = test_immediate_call()
    if call_id:
        monitor_call_progress(call_id, duration=12)
    
    # Test 4: Schedule a call
    scheduled_id = test_schedule_call()
    
    # Test 5: Get calls again
    test_get_calls()
    
    # Test 6: Delete the scheduled call
    if scheduled_id:
        test_delete_call(scheduled_id)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n💡 Open http://localhost:3001 to see the React UI!")

if __name__ == "__main__":
    run_all_tests()
