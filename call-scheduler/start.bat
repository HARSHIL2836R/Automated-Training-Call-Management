@echo off
echo ====================================
echo Starting Call Scheduler Application
echo ====================================
echo.

echo Step 1: Starting Call API (port 5000)...
start "Call API" cmd /k "cd c:\Users\Dell\Documents\GitHub\SynCoach\interview && python api_server.py"
timeout /t 3

echo Step 2: Starting Backend (port 3000)...
start "Backend" cmd /k "cd c:\Users\Dell\Documents\GitHub\SynCoach\interview\call-scheduler\backend && python app.py"
timeout /t 3

echo Step 3: Starting Frontend...
start "Frontend" cmd /k "cd c:\Users\Dell\Documents\GitHub\SynCoach\interview\call-scheduler\frontend && npm start"

echo.
echo ====================================
echo All servers are starting!
echo ====================================
echo.
echo Call API:  http://localhost:5000
echo Backend:   http://localhost:3000
echo Frontend:  http://localhost:3001 (will open automatically)
echo.
echo Press any key to exit this window...
pause > nul
