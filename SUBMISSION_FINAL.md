# Call Scheduler - Submission

## 1. Complete Source Code

The complete source code is located in the `call-scheduler/` directory:

```
call-scheduler/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
│   └── scheduler.db        # SQLite database (auto-created)
│
└── frontend/
    └── index.html          # Frontend application (HTML/CSS/JS)
```

---

## 2. Instructions on How to Run Your Application

### Prerequisites
- Python 3.8+
- The provided Call API running on `http://localhost:5000`

### Step-by-Step Instructions

#### Step 1: Start the Call API (Provided)
```bash
cd interview
pip install -r requirements.txt
python api_server.py
```
✅ Call API will run on `http://localhost:5000`

#### Step 2: Start the Backend
Open a new terminal:
```bash
cd call-scheduler/backend
pip install -r requirements.txt
python app.py
```
✅ Backend will run on `http://localhost:3000`

**Backend Dependencies:**
- Flask==3.0.0
- flask-cors==4.0.0
- APScheduler==3.10.4
- requests==2.31.0

#### Step 3: Open the Frontend
Simply open the HTML file in your browser:
```
call-scheduler/frontend/index.html
```

You can:
- Double-click the file
- Drag it into your browser
- Or use: `start call-scheduler/frontend/index.html` (Windows)

✅ The application is now ready to use!

### Quick Test
1. Enter a phone number (e.g., `+1234567890`)
2. Select a time 1-2 minutes in the future
3. Click "Schedule Call"
4. Watch the status update automatically
5. Or click "Call Now" for an immediate call

---

## 3. Brief Notes on Design Decisions and Trade-offs

### Architecture Decisions

**Backend: Flask + APScheduler + SQLite**
- **Why Flask**: Lightweight, quick to set up, perfect for REST APIs
- **Why APScheduler**: Robust background job scheduling without external dependencies
- **Why SQLite**: Persistent storage with zero configuration, perfect for demo/development

**Frontend: Vanilla HTML/CSS/JavaScript**
- **Why Not React**: Initially planned React, but pivoted to vanilla JS for faster demo (no npm build step)
- **Trade-off**: Vanilla JS is slightly more verbose but works instantly and demonstrates core web dev skills
- **Benefit**: No build process, runs immediately, same features and UI as React would have

### Key Features Implemented

1. **Schedule Future Calls** - Users can schedule calls for specific times
2. **Instant Calls** - "Call Now" button for immediate call initiation
3. **Real-time Updates** - Automatic status polling and UI refresh
4. **Call Management** - View all calls, filter by status, delete pending calls
5. **Persistent Storage** - SQLite database stores all call records

### Technical Implementation

**Background Scheduling:**
- APScheduler checks for pending calls every **30 seconds**
- When scheduled time is reached, calls are automatically initiated
- **Trade-off**: 30-second intervals balance CPU usage vs. scheduling precision

**Status Polling:**
- Active calls are polled every **5 seconds** for status updates
- Frontend refreshes the call list every **3 seconds**
- **Trade-off**: Polling is less efficient than WebSockets but works with the provided Call API

**Database Schema:**
- Single table with denormalized structure for simplicity
- Tracks: phone number, scheduled time, status, Call API ID, timestamps
- **Trade-off**: Simple for small scale, wouldn't scale to complex relationships

### Major Trade-offs

| Decision | Chosen Approach | Alternative | Reasoning |
|----------|----------------|-------------|-----------|
| **Frontend** | Vanilla JS | React | Faster demo, no build step, works instantly |
| **Database** | SQLite | PostgreSQL/MySQL | Zero config, persistent, perfect for demo |
| **Scheduler** | APScheduler | Celery | Simpler setup, no message broker needed |
| **Updates** | HTTP Polling | WebSockets | Call API doesn't support WS, polling is simpler |
| **Timezone** | Server local time | User timezone | Reduced complexity for 1-hour constraint |

### What Would I Improve With More Time

**Immediate (30 more minutes):**
- Unit tests for backend
- Retry logic for failed API calls
- Pagination for large call lists

**Production Ready (2-4 hours):**
- WebSocket implementation for real-time updates
- User authentication and authorization
- Comprehensive error logging
- Docker containerization
- Environment-based configuration

**Enterprise (1-2 days):**
- Multi-user support with role-based permissions
- Call analytics and reporting dashboard
- Recurring call scheduling
- SMS/email notifications
- Integration with multiple call providers

### Code Quality Focus

- **Clean structure**: Separated concerns (API, database, scheduling)
- **Error handling**: Try-catch blocks, user-friendly error messages
- **Documentation**: Inline comments, comprehensive README
- **Naming conventions**: Descriptive variable names, consistent patterns

### Time Breakdown

- **Backend**: ~20 minutes (Flask API + APScheduler + SQLite)
- **Frontend**: ~20 minutes (UI + API integration + real-time updates)
- **Documentation**: ~15 minutes (README, design docs)
- **Testing & Polish**: ~5 minutes

**Total**: ~60 minutes

---

## Summary

This solution demonstrates:
- ✅ Full-stack development (backend + frontend)
- ✅ External API integration
- ✅ Background job scheduling
- ✅ Real-time data updates
- ✅ Database design and SQL
- ✅ Clean, maintainable code
- ✅ Time-constrained problem-solving

The application is production-ready for a demo environment and can be easily extended with additional features.
