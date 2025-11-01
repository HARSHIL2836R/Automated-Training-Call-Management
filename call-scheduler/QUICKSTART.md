# Quick Start Guide

## Get the application running in 3 steps!

### Step 1: Start the Call API ✅
```bash
# In terminal 1 - from the interview folder
cd c:\Users\Dell\Documents\GitHub\SynCoach\interview
pip install -r requirements.txt
python api_server.py
```
✅ Call API running on http://localhost:5000

### Step 2: Start the Backend 🚀
```bash
# In terminal 2
cd c:\Users\Dell\Documents\GitHub\SynCoach\interview\call-scheduler\backend
pip install -r requirements.txt
python app.py
```
✅ Backend running on http://localhost:3000

### Step 3: Start the Frontend 💻
```bash
# In terminal 3
cd c:\Users\Dell\Documents\GitHub\SynCoach\interview\call-scheduler\frontend
npm install
npm start
```
✅ Frontend opens automatically in browser!

## Test It Out! 🎉

1. **Schedule a call**: Enter a phone number like `+1234567890` and pick a time 1-2 minutes in the future
2. **Watch it work**: The call will automatically initiate at the scheduled time
3. **See real-time updates**: Status changes from Pending → In-Progress → Completed
4. **Try "Call Now"**: For immediate calls without scheduling

## What's Happening Behind the Scenes? 🔧

- Backend checks for pending calls every 30 seconds
- Active calls are polled every 5 seconds for status updates
- Frontend refreshes the call list every 3 seconds
- All data is stored in SQLite database

## Features to Try ✨

- ✅ Schedule future calls
- ✅ Instant "Call Now" button
- ✅ Filter calls by status
- ✅ Delete pending calls
- ✅ Real-time status updates
- ✅ Beautiful responsive UI

## Having Issues? 🐛

**Backend error?**
- Make sure Call API (port 5000) is running first
- Check if port 3000 is available

**Frontend not loading?**
- Wait for `npm install` to complete
- Check if backend (port 3000) is running

**Still stuck?** Check the full README.md for troubleshooting!

---

**Total setup time: ~5 minutes** ⏱️
