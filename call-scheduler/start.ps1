# Start All Servers - PowerShell Script

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Starting Call Scheduler Application" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Start Call API
Write-Host "Step 1: Starting Call API (port 5000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Dell\Documents\GitHub\SynCoach\interview'; python api_server.py"
Start-Sleep -Seconds 3

# Step 2: Start Backend
Write-Host "Step 2: Starting Backend (port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Dell\Documents\GitHub\SynCoach\interview\call-scheduler\backend'; python app.py"
Start-Sleep -Seconds 3

# Step 3: Start Frontend
Write-Host "Step 3: Starting Frontend (will install deps if needed)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Dell\Documents\GitHub\SynCoach\interview\call-scheduler\frontend'; npm start"

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "All servers are starting!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Call API:  http://localhost:5000" -ForegroundColor White
Write-Host "Backend:   http://localhost:3000" -ForegroundColor White
Write-Host "Frontend:  http://localhost:3001 (will open automatically)" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
