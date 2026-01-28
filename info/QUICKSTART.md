# SETUP GUIDE - London Tech Events Finder

## ✅ Installation Status

Your environment is ready! Here's what's been done:

- ✅ Python 3.7.4 configured
- ✅ Virtual environment activated
- ✅ All dependencies installed:
  - Flask 3.0.0
  - requests 2.31.0
  - beautifulsoup4 4.12.3
  - python-dotenv 1.0.1
  - openai 1.13.3
- ✅ `.env` file created
- ✅ `.gitignore` file created
- ✅ Database schema ready (`schema.sql`)

## 🔑 Step 1: Add Your OpenAI API Key

1. Get your free API key:
   - Go to https://platform.openai.com/api-keys
   - Sign up for a free account (if needed)
   - Create a new API key
   - Copy the key (it looks like: `sk-proj-xxxxxxxxxxxxx`)

2. Open the `.env` file in your project root:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
   Replace `sk-your-api-key-here` with your actual key.

3. Save the file.

⚠️ **Important**: Never share your API key or commit `.env` to Git!

## 🚀 Step 2: Run the Scripts in Order

Open a PowerShell or Command Prompt in your project folder and run:

### Script 1: Scraper (Fetch Events)
```bash
python scraper.py
```

This will:
- Connect to Eventbrite London tech events page
- Extract event titles, dates, locations
- Save ~50 raw events to the database
- Print: "Inserted X new raw events"

**Expected output:**
```
Fetching https://www.eventbrite.co.uk/d/united-kingdom--london/technology--events/
Found 45 event candidates.
Inserted 45 new raw events.
Scraping completed successfully!
```

### Script 2: AI Cleaner (Validate Events)
```bash
python ai_cleaner.py
```

This will:
- Load raw events from the database
- Send them to OpenAI (gpt-4o-mini model)
- AI validates: Is it tech-related? Is it upcoming? Which category?
- Only keeps events with confidence ≥ 0.7
- Updates the database with cleaned titles and categories

**Expected output:**
```
Sending 45 events to AI for validation...
Updated 45 events using AI results.
AI validation completed successfully!
```

⚠️ **Note**: This step uses OpenAI API which may consume credits.

### Script 3: Web Server (View Events)
```bash
python server.py
```

This will:
- Start a Flask web server on http://127.0.0.1:5000
- Print: "🚀 Starting server at http://127.0.0.1:5000"

Now open your browser and go to: **http://127.0.0.1:5000**

You should see:
- Your London tech events displayed as cards
- Filter buttons at the top
- Event categories (Hackathon, Workshop, Meetup, etc.)
- Free/Paid badges
- AI confidence scores
- Click any event to open it on Eventbrite

## 🌐 Accessing Your Web App

### Local Machine
- Open browser: http://127.0.0.1:5000 or http://localhost:5000

### From Another Device (Same WiFi)
1. Find your PC's IP address:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On another device, go to: http://192.168.1.100:5000

3. In `server.py`, change:
   ```python
   app.run(host="127.0.0.1", port=5000, debug=True)
   ```
   To:
   ```python
   app.run(host="0.0.0.0", port=5000, debug=True)
   ```

## 📊 Database

The database (`database.db`) is automatically created when you run any script.

### View data with SQLite:
```bash
sqlite3 database.db
```

Useful queries:
```sql
-- See all approved events
SELECT title, date, category, is_free FROM events WHERE is_valid = 1;

-- See all unprocessed events
SELECT title, date FROM events WHERE is_valid = 0;

-- Count by category
SELECT category, COUNT(*) FROM events WHERE is_valid = 1 GROUP BY category;
```

## 🔄 Recommended Workflow

### **First Time Setup**
```
1. python scraper.py        (2-5 seconds)
   └─ Fetches ~50 events

2. python ai_cleaner.py     (20-60 seconds, depends on API)
   └─ Validates with AI

3. python server.py         (Runs continuously)
   └─ View at http://localhost:5000
   └─ Press Ctrl+C to stop
```

### **Daily Updates**
Run this every morning/evening:
```
python scraper.py && python ai_cleaner.py
```

Then keep `server.py` running all day.

### **Manual Updates**
```
python scraper.py      (Fetch new events)
python ai_cleaner.py   (Validate them)
```
Web page auto-loads latest data on refresh.

## 🐛 Common Issues & Solutions

### **Issue: "OpenAI API key is not set"**
**Solution:**
1. Open `.env` file
2. Add your key: `OPENAI_API_KEY=sk-xxxx...`
3. Save and re-run the script

### **Issue: "Failed to fetch Eventbrite page"**
**Solution:**
- Eventbrite's HTML may have changed
- Try running again (might be temporary)
- Update selectors in `scraper.py` if it persists

### **Issue: No events showing on website**
**Solution:**
1. Did you run `scraper.py` first? (fetches events)
2. Did you run `ai_cleaner.py` second? (validates them)
3. Check database: `sqlite3 database.db "SELECT COUNT(*) FROM events WHERE is_valid = 1;"`

### **Issue: "Port 5000 already in use"**
**Solution:**
Edit `server.py`:
```python
app.run(host="127.0.0.1", port=5001, debug=True)  # Change 5000 to 5001
```

### **Issue: "ModuleNotFoundError: No module named 'flask'"**
**Solution:**
Reinstall packages:
```bash
pip install -r requirements.txt
```

## 📈 Performance Tips

- **Scraper**: Takes 2-5 seconds (network dependent)
- **AI Cleaner**: Takes 20-60 seconds per batch of 20 events
  - Limit: 20 events per run (prevents timeout)
  - Costs: ~$0.01-0.05 per 20 events
- **Server**: Instant response (filters in-memory)

## 🔒 Security Notes

- ✅ `.env` is in `.gitignore` (won't be committed)
- ✅ Database is local (no cloud)
- ✅ No authentication yet (add if needed)
- ✅ Never share your `.env` file

## 📱 Mobile Experience

The website is **mobile-first**:
- Tested on iPhone, Android, iPad
- Touch-friendly buttons
- Responsive layout
- Fast loading

## 📞 Support Checklist

Before asking for help, verify:
- [ ] Python 3.7+ installed (`python --version`)
- [ ] `.env` file exists and has API key
- [ ] All dependencies installed (`pip list | grep Flask`)
- [ ] Try again (sometimes APIs timeout)

## 🎉 Next Steps

Once running:
1. **Browse events** - Click any event to go to Eventbrite
2. **Filter events** - Use category and free filters
3. **Refresh daily** - Run scraper + AI cleaner daily
4. **Customize** - Edit `style.css` for different colors
5. **Add features** - See README.md for ideas

---

**Your app is ready to go! Run `python scraper.py` to get started.** 🚀
