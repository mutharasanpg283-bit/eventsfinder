# START HERE - Getting Your App Running in 3 Steps

## Status: ✅ READY TO GO

Your London Tech Events Finder is fully installed and configured!

---

## Step 1: Get Your OpenAI API Key (2 minutes)

1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (looks like: `sk-proj-xxxxxxxxxxxxxxxxxxxxx`)
4. Open the `.env` file in this folder
5. Replace the placeholder with your real key:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```
6. Save the file

**Note**: This key is free to generate. You get $5 free credits to start.

---

## Step 2: Fetch Events (2-5 seconds)

Open PowerShell in this folder and run:

```bash
python scraper.py
```

**What it does**:
- Connects to Eventbrite
- Finds tech events in London
- Extracts ~50 events
- Saves them to database

**Expected output**:
```
Fetching https://www.eventbrite.co.uk/d/united-kingdom--london/technology--events/
Found 45 event candidates.
Inserted 45 new raw events.
Scraping completed successfully!
```

---

## Step 3: Run the Web Server (Stays running)

Keep PowerShell open and run:

```bash
python server.py
```

**What it does**:
- Starts a local web server
- Validates events with AI
- Displays them on a website

**Expected output**:
```
🚀 Starting server at http://127.0.0.1:5000
⚠️  Press Ctrl+C to stop
```

Then:
1. **Open your browser**
2. **Go to**: http://127.0.0.1:5000
3. **You'll see**: Event cards from London

---

## Features You Can Use Right Now

✅ **View Events** - See title, date, location  
✅ **Filter by Category** - Hackathon, Workshop, Meetup, Conference  
✅ **Filter by Price** - Free events only  
✅ **Click to Visit** - Opens Eventbrite event page  
✅ **AI Confidence Score** - See how confident the AI was  

---

## File Overview

```
Your Project Folder:
├── README.md ..................... Full documentation
├── QUICKSTART.md ................. Step-by-step setup guide  
├── ARCHITECTURE.md ............... Technical details
├── INSTALLATION_COMPLETE.md ...... What got installed
│
├── scraper.py .................... Fetches events (run 1st)
├── ai_cleaner.py ................. Validates with AI (run 2nd)
├── server.py ..................... Web server (run 3rd)
│
├── database.db ................... Local event database
├── schema.sql .................... Database structure
│
├── templates/index.html .......... Web page
├── static/style.css .............. Styling
├── static/app.js ................. Filtering logic
│
├── requirements.txt .............. Python dependencies
├── .env .......................... Your API key goes here
└── .gitignore .................... Prevents accidents
```

---

## Common Questions

### Q: Why won't it start?
A: Did you add your OpenAI API key to `.env`? That's required for step 2.

### Q: I don't see any events
A: Make sure you ran both:
1. `python scraper.py` (fetches events)
2. Then server starts automatically

### Q: Can I use a different port?
A: Yes! Edit line in `server.py`:
```python
app.run(host="127.0.0.1", port=5001, debug=True)  # Change 5000 to 5001
```

### Q: How do I stop the server?
A: Press `Ctrl+C` in the terminal

### Q: Can friends access it?
A: To let others on your WiFi see it:
- Find your IP: `ipconfig` (look for IPv4 Address like 192.168.1.100)
- In server.py, change `host="127.0.0.1"` to `host="0.0.0.0"`
- They can then visit: `http://192.168.1.100:5000`

---

## Next: Automate Daily Updates

To get fresh events every day, create a batch file:

**Windows - Create `update_events.bat`**:
```batch
@echo off
cd c:\Users\mutha\Desktop\event
venv\Scripts\python.exe scraper.py
venv\Scripts\python.exe ai_cleaner.py
echo Events updated!
pause
```

Then use **Task Scheduler** to run it daily at 8 AM.

---

## Get More Help

| Topic | File to Read |
|-------|------------|
| Complete guide | README.md |
| Beginner walkthrough | QUICKSTART.md |
| Technical details | ARCHITECTURE.md |
| What got installed | INSTALLATION_COMPLETE.md |

---

## Your Next Move

### Right Now:
1. ✏️ Edit `.env` with your API key
2. ▶️ Run `python scraper.py`
3. ▶️ Run `python server.py`
4. 🌐 Open http://127.0.0.1:5000

### Today:
- Browse events
- Test filters
- Try different categories

### This Week:
- Set up daily automation
- Customize colors in style.css
- Add more event sources

---

## Technology Summary

| What | Tech | Version |
|------|------|---------|
| Python | Python | 3.7.4 |
| Web Server | Flask | 2.2.5 |
| AI Validation | OpenAI API | gpt-4o-mini |
| Database | SQLite | Built-in |
| Frontend | HTML/CSS/JS | Vanilla |

**Everything works locally - no cloud needed!** 🚀

---

## Questions or Issues?

### Check Database Directly
```bash
sqlite3 database.db
SELECT COUNT(*) FROM events WHERE is_valid = 1;
SELECT title, date FROM events LIMIT 5;
.quit
```

### Check Event Details
```bash
# See all events (approved)
SELECT * FROM events WHERE is_valid = 1;

# See by category
SELECT * FROM events WHERE category = 'Hackathon' AND is_valid = 1;

# See stats
SELECT category, COUNT(*) FROM events WHERE is_valid = 1 GROUP BY category;
```

---

## You're All Set!

Your application is ready. No more setup needed.

**GO**: Open your terminal, add your API key to `.env`, and run:

```bash
python scraper.py && python server.py
```

Then visit: **http://127.0.0.1:5000**

Enjoy your London tech events finder! 🎉

---

**Made with ❤️ - Keep it simple, keep it local**
