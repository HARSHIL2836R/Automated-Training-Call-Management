import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:3000';

function App() {
  const [calls, setCalls] = useState([]);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [scheduledTime, setScheduledTime] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');

  // Fetch calls on mount and every 3 seconds
  useEffect(() => {
    fetchCalls();
    const interval = setInterval(fetchCalls, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchCalls = async () => {
    try {
      const response = await fetch(`${API_URL}/api/calls`);
      const data = await response.json();
      if (data.success) {
        setCalls(data.calls);
      }
    } catch (err) {
      console.error('Error fetching calls:', err);
    }
  };

  const scheduleCall = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/schedule`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone_number: phoneNumber,
          scheduled_time: scheduledTime,
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setPhoneNumber('');
        setScheduledTime('');
        fetchCalls();
      } else {
        setError(data.error || 'Failed to schedule call');
      }
    } catch (err) {
      setError('Network error. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const callNow = async () => {
    if (!phoneNumber) {
      setError('Please enter a phone number');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/call-now`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: phoneNumber }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setPhoneNumber('');
        fetchCalls();
      } else {
        setError(data.error || 'Failed to initiate call');
      }
    } catch (err) {
      setError('Network error. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const deleteCall = async (id) => {
    try {
      const response = await fetch(`${API_URL}/api/calls/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        fetchCalls();
      } else {
        const data = await response.json();
        alert(data.error || 'Failed to delete call');
      }
    } catch (err) {
      alert('Network error');
    }
  };

  const getDefaultDateTime = () => {
    const now = new Date();
    now.setMinutes(now.getMinutes() + 5);
    return now.toISOString().slice(0, 16);
  };

  const filteredCalls = calls.filter((call) => {
    if (filter === 'all') return true;
    return call.status === filter;
  });

  const getStatusBadge = (status) => {
    const badges = {
      pending: '⏳ Pending',
      'in-progress': '📞 In Progress',
      completed: '✅ Completed',
      failed: '❌ Failed',
    };
    return badges[status] || status;
  };

  const getCallStatusBadge = (callStatus) => {
    if (!callStatus) return '';
    const badges = {
      initiated: '🔵 Initiated',
      ringing: '🔔 Ringing',
      connected: '📞 Connected',
      completed: '✅ Completed',
    };
    return badges[callStatus] || callStatus;
  };

  const formatDateTime = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📞 Call Scheduler</h1>
        <p>Schedule and manage your calls</p>
      </header>

      <div className="container">
        {/* Schedule Form */}
        <div className="card">
          <h2>Schedule a Call</h2>
          <form onSubmit={scheduleCall}>
            <div className="form-group">
              <label>Phone Number:</label>
              <input
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="+1234567890"
                required
                minLength="10"
              />
            </div>

            <div className="form-group">
              <label>Scheduled Time:</label>
              <input
                type="datetime-local"
                value={scheduledTime}
                onChange={(e) => setScheduledTime(e.target.value + ':00')}
                required
                min={getDefaultDateTime()}
              />
            </div>

            {error && <div className="error">{error}</div>}

            <div className="button-group">
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? 'Scheduling...' : 'Schedule Call'}
              </button>
              <button
                type="button"
                onClick={callNow}
                disabled={loading}
                className="btn-secondary"
              >
                Call Now
              </button>
            </div>
          </form>
        </div>

        {/* Calls List */}
        <div className="card">
          <div className="card-header">
            <h2>Scheduled Calls ({filteredCalls.length})</h2>
            <div className="filter-buttons">
              <button
                className={filter === 'all' ? 'active' : ''}
                onClick={() => setFilter('all')}
              >
                All
              </button>
              <button
                className={filter === 'pending' ? 'active' : ''}
                onClick={() => setFilter('pending')}
              >
                Pending
              </button>
              <button
                className={filter === 'in-progress' ? 'active' : ''}
                onClick={() => setFilter('in-progress')}
              >
                In Progress
              </button>
              <button
                className={filter === 'completed' ? 'active' : ''}
                onClick={() => setFilter('completed')}
              >
                Completed
              </button>
            </div>
          </div>

          {filteredCalls.length === 0 ? (
            <p className="empty-state">No calls scheduled yet</p>
          ) : (
            <div className="calls-list">
              {filteredCalls.map((call) => (
                <div key={call.id} className="call-item">
                  <div className="call-info">
                    <div className="call-number">{call.phone_number}</div>
                    <div className="call-time">
                      {formatDateTime(call.scheduled_time)}
                    </div>
                    <div className="call-badges">
                      <span className={`badge status-${call.status}`}>
                        {getStatusBadge(call.status)}
                      </span>
                      {call.call_status && (
                        <span className="badge call-status">
                          {getCallStatusBadge(call.call_status)}
                        </span>
                      )}
                    </div>
                    {call.error_message && (
                      <div className="error-msg">⚠️ {call.error_message}</div>
                    )}
                  </div>
                  <div className="call-actions">
                    {call.status === 'pending' && (
                      <button
                        onClick={() => deleteCall(call.id)}
                        className="btn-delete"
                        title="Delete call"
                      >
                        🗑️
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <footer>
        <p>Backend running on localhost:3000 | Call API on localhost:5000</p>
      </footer>
    </div>
  );
}

export default App;
