# Call Scheduler - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │          React Frontend (Port 3001)                   │    │
│  │                                                        │    │
│  │  • Schedule Call Form                                 │    │
│  │  • Call List Display                                  │    │
│  │  • Real-time Status Updates (refresh every 3s)        │    │
│  │  • Filter & Delete Controls                           │    │
│  └────────────────┬──────────────────────────────────────┘    │
└───────────────────┼──────────────────────────────────────────┘
                    │
                    │ HTTP Requests
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│          Flask Backend Server (Port 3000)                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  REST API Endpoints:                                      │  │
│  │  • POST /api/schedule     - Schedule a call             │  │
│  │  • POST /api/call-now     - Immediate call              │  │
│  │  • GET  /api/calls        - Get all calls               │  │
│  │  • GET  /api/calls/:id    - Get specific call           │  │
│  │  • DELETE /api/calls/:id  - Delete pending call         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                    │                          │                 │
│                    ▼                          ▼                 │
│  ┌─────────────────────────┐   ┌──────────────────────────┐   │
│  │   APScheduler           │   │   SQLite Database        │   │
│  │   Background Jobs:      │   │   (scheduler.db)         │   │
│  │                         │   │                          │   │
│  │  • Check pending calls  │   │  Table: scheduled_calls  │   │
│  │    (every 30 seconds)   │◄──┤  • id                    │   │
│  │                         │   │  • phone_number          │   │
│  │  • Poll active calls    │   │  • scheduled_time        │   │
│  │    (every 5 seconds)    │   │  • status                │   │
│  │                         │   │  • call_api_id           │   │
│  └──────────┬──────────────┘   │  • call_status           │   │
│             │                   │  • created_at            │   │
└─────────────┼───────────────────│  • updated_at            │───┘
              │                   │  • error_message         │
              │                   └──────────────────────────┘
              │ HTTP Requests
              ▼
┌─────────────────────────────────────────────────────────────────┐
│         External Call API (Port 5000) - PROVIDED               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Endpoints:                                               │  │
│  │  • POST /api/call        - Initiate a call               │  │
│  │  • GET  /api/call/:id    - Get call status               │  │
│  │                                                           │  │
│  │  Call Status Progression:                                │  │
│  │  initiated → ringing → connected → completed             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Schedule a Call
```
User fills form in React
    ↓
POST /api/schedule to Backend
    ↓
Backend saves to SQLite
    ↓
Returns success to Frontend
    ↓
Frontend refreshes call list
```

### 2. Automatic Call Initiation
```
APScheduler runs every 30 seconds
    ↓
Checks SQLite for pending calls where scheduled_time <= now
    ↓
For each pending call:
    POST /api/call to Call API
    ↓
Call API returns call_id and status
    ↓
Backend updates SQLite (status = 'in-progress')
```

### 3. Status Updates
```
APScheduler runs every 5 seconds
    ↓
Checks SQLite for in-progress calls
    ↓
For each in-progress call:
    GET /api/call/:id from Call API
    ↓
Updates call_status in SQLite
    ↓
If status = 'completed', mark as done
    
Meanwhile, every 3 seconds:
Frontend refreshes call list via GET /api/calls
    ↓
Displays updated statuses to user
```

## Technology Stack

### Frontend
- **React 18** - Component-based UI
- **Functional Components** - Modern hooks-based state
- **CSS3** - Responsive gradient design
- **Fetch API** - HTTP requests to backend

### Backend
- **Flask 3.0** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **APScheduler 3.10** - Background job scheduling
- **Requests 2.31** - HTTP client for Call API
- **SQLite 3** - Embedded database

### Database Schema
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

## Call Status States

### Our Application Status
- **pending** - Scheduled, waiting for time
- **in-progress** - Call initiated with API
- **completed** - Call finished successfully
- **failed** - Failed to initiate

### Call API Status (for in-progress calls)
- **initiated** - Call just started
- **ringing** - Phone is ringing
- **connected** - Call connected
- **completed** - Call ended

## Timing Configuration

| Component | Action | Frequency | Reason |
|-----------|--------|-----------|--------|
| Backend | Check pending calls | 30 seconds | Balance CPU vs responsiveness |
| Backend | Poll active calls | 5 seconds | Real-time updates |
| Frontend | Refresh UI | 3 seconds | Keep user informed |

## File Structure

```
call-scheduler/
│
├── backend/
│   ├── app.py                 # Flask application (290 lines)
│   │   ├── Database initialization
│   │   ├── API endpoints (6 routes)
│   │   ├── Background jobs (2 schedulers)
│   │   └── Call API integration
│   │
│   ├── requirements.txt       # Python dependencies
│   └── scheduler.db          # SQLite database (auto-created)
│
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML template
│   │
│   ├── src/
│   │   ├── App.js            # Main React component (280 lines)
│   │   │   ├── State management
│   │   │   ├── API calls
│   │   │   ├── Form handling
│   │   │   └── UI rendering
│   │   │
│   │   ├── App.css           # Styling (380 lines)
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   │
│   └── package.json          # Node dependencies
│
├── start.bat                  # Windows startup script
├── start.ps1                  # PowerShell startup script
├── test_scheduler.py         # Automated tests
│
└── Documentation/
    ├── README.md             # Full documentation
    ├── QUICKSTART.md         # Quick start guide
    ├── DESIGN_DECISIONS.md  # Design rationale
    ├── SUBMISSION.md         # Submission overview
    ├── STATUS.md             # Current status
    └── ARCHITECTURE.md       # This file
```

## Security Considerations

### Implemented
- ✅ CORS properly configured
- ✅ Input validation (phone numbers)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Error handling throughout

### Not Implemented (Time constraint)
- ❌ Authentication/Authorization
- ❌ Rate limiting
- ❌ HTTPS/SSL
- ❌ Input sanitization (comprehensive)
- ❌ API key management

## Scalability Considerations

### Current Implementation
- **Good for**: Demo, small teams, development
- **Handles**: ~100 concurrent calls easily
- **Limitations**: 
  - Single server
  - In-process scheduler
  - SQLite (file-based)

### Production Improvements
- Replace polling with WebSockets
- Use PostgreSQL instead of SQLite
- Separate scheduler service (Celery)
- Load balancer for multiple instances
- Redis for caching
- Message queue for reliability

## Error Handling

### Backend
- Try-catch blocks around external API calls
- Database error handling
- Validation errors returned to frontend
- Logging for debugging

### Frontend
- Network error detection
- User-friendly error messages
- Graceful degradation
- Loading states

## Performance Optimizations

### Backend
- Indexes on SQLite (id, status)
- Only poll active calls, not all calls
- Batch processing in scheduler

### Frontend
- Debounced API calls
- Conditional rendering
- CSS animations (GPU accelerated)
- Minimal re-renders

## Testing Strategy

### Automated Tests (test_scheduler.py)
- Health checks for both servers
- Schedule call endpoint
- Immediate call endpoint
- Get calls endpoint
- Delete call endpoint
- Status progression monitoring

### Manual Testing
- UI interaction testing
- Real-time update verification
- Error scenario testing
- Cross-browser compatibility

---

**This architecture provides a solid foundation for a call scheduling system that can be extended with additional features as needed.**
