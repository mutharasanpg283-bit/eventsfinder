# ✅ AUTONOMOUS SYSTEM - LAUNCH CHECKLIST

## Pre-Launch Verification

### 1. Python Environment
- [x] Python 3.7.4 installed
- [x] Virtual environment created: `venv/`
- [x] All packages installed: `requirements.txt`
- [x] Activation works: `venv\Scripts\Activate` (Windows)

**Verify:**
```bash
python --version  # Should show 3.7.4+
pip list | grep Flask  # Should show Flask 2.2.5
```

### 2. Configuration
- [x] `.env` file created
- [x] OpenAI API key set in `.env`
- [x] Database schema ready: `schema.sql`

**Verify:**
```bash
cat .env  # Check OPENAI_API_KEY is set
ls -la database.db  # Database will be created on first run
```

### 3. Core Modules
- [x] `main.py` - Orchestrator
- [x] `scraper.py` - Original scraper
- [x] `scraper_advanced.py` - Multi-source scraper
- [x] `ai_cleaner.py` - AI validation
- [x] `server.py` - Web server
- [x] `continuous_runner.py` - Autonomous loop (NEW!)
- [x] `source_discovery.py` - Discovery engine (NEW!)

**Verify:**
```bash
python -c "import main, scraper_advanced, ai_cleaner, server, continuous_runner, source_discovery; print('✓ All modules import successfully!')"
```

### 4. Frontend
- [x] `templates/index.html` - Web interface
- [x] `static/app.js` - Frontend logic
- [x] `static/style.css` - Styling

**Verify:**
```bash
ls templates/index.html static/app.js static/style.css
```

### 5. Documentation
- [x] README.md
- [x] START_HERE.md
- [x] QUICKSTART.md
- [x] CONTINUOUS_DISCOVERY_GUIDE.md (NEW!)
- [x] CONTINUOUS_QUICK_REF.md (NEW!)
- [x] SYSTEM_READY.md (NEW!)
- [x] PROJECT_COMPLETE.md (NEW!)
- [x] Additional guides: ARCHITECTURE.md, DEPLOYMENT.md, etc.

---

## Pre-Launch Testing

### Test 1: Module Imports ✓
```bash
python -c "import main; import continuous_runner; import source_discovery; print('✓ All modules load')"
# Result: ✓ All modules load
```

### Test 2: Database Setup ✓
```bash
python -c "
from pathlib import Path
import sqlite3
from scraper_advanced import EventScraper
scraper = EventScraper()
conn = scraper.init_db()
conn.close()
print('✓ Database initialized')
"
# Result: ✓ Database initialized
```

### Test 3: Scraper Works ✓
```bash
python scraper_advanced.py
# Results in output:
# 🚀 LONDON TECH EVENTS SCRAPER - MULTI-SOURCE
# ✓ Found X events from Y sources
# ✓ Scraping completed successfully!
```

### Test 4: Discovery Ready ✓
```bash
python -c "import source_discovery; print('✓ Discovery module ready')"
# Result: ✓ Discovery module ready
```

### Test 5: Continuous Runner Ready ✓
```bash
python -c "import continuous_runner; print('✓ Continuous runner ready')"
# Result: ✓ Continuous runner ready
```

---

## Launch Procedures

### Procedure A: Test Run (Recommended First)
```bash
# 1. Start source discovery once
python source_discovery.py

# Expected output:
# 🤖 SOURCE DISCOVERY CYCLE - Machine Learning Mode
# ✨ Discovered sources
# ✅ SCRAPING COMPLETE
# [Exits after 1 cycle]

# Time: ~5-10 minutes
# Next step: Check database.db was created
```

### Procedure B: Full Manual Scrape
```bash
# 1. Scrape once
python scraper_advanced.py

# 2. Validate with AI
python ai_cleaner.py

# 3. Start server only
python main.py --serve-only

# 4. View in browser: http://127.0.0.1:5000

# Time: ~10-30 minutes
# Result: See real events!
```

### Procedure C: Full Autonomous System (MAIN)
```bash
# Start the continuous runner
python continuous_runner.py

# Expected output:
# 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
# AUTONOMOUS CONTINUOUS EVENT DISCOVERY & SCRAPING SYSTEM
# 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
# 
# ⚙️ CONFIGURATION
# ✨ System is fully autonomous
# 💡 Press Ctrl+C to stop
# 
# 🔄 INITIAL STARTUP SEQUENCE
# [Running discovery & scraping...]
# 📊 CONTINUOUS RUNNER STATUS
# [Shows current stats]
# ⏳ Next cycle in 30 minutes...

# Time: Runs forever (until Ctrl+C)
# Monitor: Watch discovered_sources.json and database.db grow
```

---

## First-Time Launch Walkthrough

### Step 1: Verify Everything (2 minutes)
```bash
cd C:\Users\mutha\Desktop\event
venv\Scripts\Activate
python -c "import continuous_runner, source_discovery; print('✓ Ready')"
```

### Step 2: Start the System (1 minute)
```bash
python continuous_runner.py
```

### Step 3: Let It Run (30 minutes minimum)
```
Watch the output:
- Discovery phase (searches web)
- Scraping phase (fetches events)
- Validation phase (AI checks quality)
- Status summary (shows progress)

Key indicators:
✓ "Found X events" = scraping working
✓ "Discovered Y sources" = discovery working
✓ "Added Z sources" = learning happening
```

### Step 4: Monitor Progress (in another terminal)
```bash
# Terminal 1: Keep continuous_runner running
# Terminal 2: Check progress

# Check sources found
python -c "import json; s=json.load(open('discovered_sources.json')); print(f'{len(s)} sources')"

# Check events
python -c "import sqlite3; c=sqlite3.connect('database.db'); print(f'{c.cursor().execute(\"SELECT COUNT(*) FROM events\").fetchone()[0]} events')"

# View events at
# http://127.0.0.1:5000
```

---

## Expected Timeline

### First 10 Minutes
```
✓ Module initialization
✓ Database created
✓ First discovery starts
✓ First scrape starts
✓ Web server ready
```

### First 30 Minutes
```
✓ Initial discovery cycle complete
✓ 30-60 events found
✓ 5-10 new sources discovered
✓ AI validation in progress
```

### First 2 Hours
```
✓ Multiple discovery cycles
✓ 100+ events total
✓ 15-20 sources discovered
✓ Second scrape cycle complete
✓ Strong patterns emerging
```

### First 24 Hours
```
✓ Many discovery cycles
✓ 500-1000+ events
✓ 75-100+ sources discovered
✓ Multiple scrape cycles
✓ AI validation catching spam
✓ System self-improving
```

---

## Monitoring Dashboard

### Watch System in Real-Time

**Terminal 1 (Main Process):**
```bash
python continuous_runner.py --verbose
# Shows all activities with timestamps
```

**Terminal 2 (Progress Monitor):**
```bash
# Run every 30 seconds to watch growth
while true; do
  clear
  python -c "
  import json, sqlite3
  s = json.load(open('discovered_sources.json'))
  c = sqlite3.connect('database.db')
  cur = c.cursor()
  cur.execute('SELECT COUNT(*) FROM events')
  total = cur.fetchone()[0]
  cur.execute('SELECT COUNT(*) FROM events WHERE is_valid=1')
  valid = cur.fetchone()[0]
  print('📊 SYSTEM STATUS')
  print(f'  Sources: {len(s)}')
  print(f'  Total Events: {total}')
  print(f'  Validated: {valid}')
  print(f'  Pending: {total - valid}')
  "
  sleep 30
done
```

**Browser:**
```
Open: http://127.0.0.1:5000
Shows: All validated events in real-time
Auto-updates: As new events are validated
```

---

## Configuration Options

### Default (Balanced)
```bash
python continuous_runner.py
# Discovery: Every 30 minutes
# Scraping: Every 6 hours
# Best for: Balanced growth
```

### Fast (Aggressive)
```bash
python continuous_runner.py --discovery 10 --scrape 60
# Discovery: Every 10 minutes
# Scraping: Every hour
# Best for: Maximum events/growth
```

### Slow (Gentle)
```bash
python continuous_runner.py --discovery 60 --scrape 1440
# Discovery: Every hour
# Scraping: Every day
# Best for: Respectful to servers
```

### Debug (Verbose)
```bash
python continuous_runner.py --verbose
# Shows all logs in real-time
# Best for: Understanding what's happening
```

---

## Troubleshooting During Launch

### Issue: "Module not found"
```
Solution:
1. Activate venv: venv\Scripts\Activate
2. Install missing package: pip install -r requirements.txt
3. Try again
```

### Issue: "OPENAI_API_KEY not set"
```
Solution:
1. Open .env file
2. Check OPENAI_API_KEY=your_key is present
3. Make sure there are no extra spaces
4. Restart continuous_runner.py
```

### Issue: "Database is locked"
```
Solution:
1. Stop continuous_runner.py (Ctrl+C)
2. Delete database.db: rm database.db
3. Start again: python continuous_runner.py
```

### Issue: "Connection timeout"
```
Solution:
1. Check internet connection
2. Some sites block scraping - this is normal
3. System will retry in next cycle
4. No action needed
```

### Issue: "No events found"
```
Solution:
1. Let it run for at least 1 hour
2. Check database: sqlite3 database.db "SELECT COUNT(*) FROM events"
3. If 0 after 1 hour, check OpenAI API key
4. Check internet connection
```

---

## Success Criteria

### ✅ System is Working If:

**After 10 minutes:**
- [ ] No error messages
- [ ] "CONTINUOUS RUNNER STATUS" displays
- [ ] Numbers are non-zero or increasing

**After 30 minutes:**
- [ ] Sources found: 5+
- [ ] Events found: 30+
- [ ] Discovery running without errors

**After 2 hours:**
- [ ] Sources discovered: 15+
- [ ] Total events: 100+
- [ ] Validated events: 50+
- [ ] Web server accessible at http://127.0.0.1:5000

**After 24 hours:**
- [ ] Sources discovered: 50+
- [ ] Total events: 500+
- [ ] Validated: 300+
- [ ] discovered_sources.json file growing
- [ ] database.db file growing

### 🚨 Issues If:

- [ ] No output for 5 minutes (check terminal)
- [ ] Same numbers for 1 hour (check API key)
- [ ] "Connection error" repeated (check internet)
- [ ] Web server not accessible (port 5000 in use?)

---

## Next Steps After Launch

### Immediate (First Hour)
1. Monitor output
2. Check web interface
3. Verify discovery is working

### Short Term (First Day)
1. Let system run 24 hours
2. Monitor growth in database
3. Check discovered_sources.json

### Medium Term (First Week)
1. Adjust settings if needed (--discovery, --scrape)
2. Add custom search queries (edit source_discovery.py)
3. Optimize performance based on stats

### Long Term (Production)
1. Deploy to VPS (see DEPLOYMENT.md)
2. Set up monitoring (uptime, errors)
3. Configure backups (database.db)
4. Enable HTTPS (security)

---

## Quick Commands Reference

```bash
# Start system
python continuous_runner.py

# Start with options
python continuous_runner.py --discovery 10 --scrape 60 --verbose

# Test discovery only (once)
python source_discovery.py

# Test scraper only (once)
python scraper_advanced.py

# Check sources
python -c "import json; print(f'{len(json.load(open(\"discovered_sources.json\")))} sources')"

# Check events
python -c "import sqlite3; print(f'{sqlite3.connect(\"database.db\").cursor().execute(\"SELECT COUNT(*) FROM events\").fetchone()[0]} events')"

# Check validated
python -c "import sqlite3; c=sqlite3.connect('database.db'); print(f'{c.cursor().execute(\"SELECT COUNT(*) FROM events WHERE is_valid=1\").fetchone()[0]} validated')"

# View web server
# http://127.0.0.1:5000

# Stop system (when running)
# Ctrl+C

# Delete and restart (fresh start)
# Ctrl+C, then: rm database.db, then: python continuous_runner.py
```

---

## Final Checklist

Before launching, confirm:

- [ ] Python 3.7+ installed
- [ ] Virtual environment activated
- [ ] All packages installed
- [ ] .env file has OpenAI API key
- [ ] Internet connection works
- [ ] No other process on port 5000
- [ ] database.db deleted (fresh start)
- [ ] Read START_HERE.md or CONTINUOUS_QUICK_REF.md

---

## 🚀 You're Ready!

```bash
python continuous_runner.py
```

**Your autonomous event discovery system is launching! 🤖**

Watch it discover sources, scrape events, and validate with AI - all automatically!

Good luck! 🎉
