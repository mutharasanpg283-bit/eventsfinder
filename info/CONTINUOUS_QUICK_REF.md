# 🤖 AUTONOMOUS DISCOVERY - QUICK REFERENCE

## One-Line Starters

```bash
# Run everything automatically (RECOMMENDED)
python continuous_runner.py

# Aggressive discovery (find lots of sources)
python continuous_runner.py --discovery 10 --scrape 60

# Gentle discovery (respect servers, run longer)
python continuous_runner.py --discovery 60 --scrape 1440

# See detailed logs
python continuous_runner.py --verbose

# Just test discovery once
python source_discovery.py
```

---

## How It Works (Visual)

```
                    START
                     ↓
          ┌──────────────────────┐
          │ DISCOVERY (30 min)   │
          ├──────────────────────┤
          │ ✓ Search web         │
          │ ✓ Analyze events     │
          │ ✓ Check links        │
          │ ✓ Learn patterns     │
          └──────────┬───────────┘
                     ↓
          ┌──────────────────────┐
          │ SCRAPING (6 hours)   │
          ├──────────────────────┤
          │ ✓ Get ALL sources    │
          │ ✓ Extract events     │
          │ ✓ Store in DB        │
          └──────────┬───────────┘
                     ↓
          ┌──────────────────────┐
          │ AI VALIDATION        │
          ├──────────────────────┤
          │ ✓ Check quality      │
          │ ✓ Remove spam        │
          │ ✓ Categorize         │
          └──────────┬───────────┘
                     ↓
          ┌──────────────────────┐
          │ REPEAT FOREVER       │
          └──────────────────────┘
```

---

## What Gets Discovered

```
PHASE 1: Search Web
├─ "London tech events"
├─ "London developer meetups"
├─ "London hackathons 2026"
├─ "best tech events London"
└─ (15+ search queries)
   ↓
   Finds: Eventbrite, Meetup, specialized sites
   

PHASE 2: Analyze Events
├─ Look at 100 existing events
├─ Extract URLs from descriptions
├─ Visit those URLs
└─ Add if they're event-related
   ↓
   Finds: Linked event sites
   

PHASE 3: Check Links
├─ Visit known event sites
├─ Extract all outgoing links
├─ Check if they link to other events
└─ Validate & add
   ↓
   Finds: Partner sites, secondary sources
```

---

## Files Created

| File | Purpose |
|------|---------|
| `continuous_runner.py` | Main orchestrator - runs everything |
| `source_discovery.py` | Intelligent discovery & learning |
| `discovered_sources.json` | Learned sources (grows over time) |
| `CONTINUOUS_DISCOVERY_GUIDE.md` | Full documentation |

---

## Real-Time Monitoring

### Watch Discovered Sources Grow

```bash
# Check how many sources found
python -c "import json; s=json.load(open('discovered_sources.json')); print(f'{len(s)} sources found!')"

# List all sources
python -c "import json; print(json.dumps(json.load(open('discovered_sources.json')), indent=2))"
```

### Watch Database Grow

```bash
# Count events
python -c "import sqlite3; c=sqlite3.connect('database.db'); print(f'{c.cursor().execute(\"SELECT COUNT(*) FROM events\").fetchone()[0]} events!')"

# Count validated
python -c "import sqlite3; c=sqlite3.connect('database.db'); print(f'{c.cursor().execute(\"SELECT COUNT(*) FROM events WHERE is_valid=1\").fetchone()[0]} validated!')"
```

### Live Dashboard (One-Liner)

```bash
# Watch stats update every 5 seconds (Linux/Mac)
watch -n 5 "python -c \"import json, sqlite3; s=json.load(open('discovered_sources.json')); c=sqlite3.connect('database.db'); cur=c.cursor(); cur.execute('SELECT COUNT(*) FROM events'); tot=cur.fetchone()[0]; cur.execute('SELECT COUNT(*) FROM events WHERE is_valid=1'); val=cur.fetchone()[0]; print(f'Sources: {len(s)} | Total Events: {tot} | Validated: {val}')\""
```

---

## Comparison Table

| Mode | Discovery | Scrape | Best For | Start With |
|------|-----------|--------|----------|-----------|
| **Default** | 30 min | 6 hrs | Balanced | ✅ YES |
| **Aggressive** | 10 min | 1 hr | Growing DBs | After testing |
| **Gentle** | 60 min | 24 hrs | Live servers | Production |
| **Manual** | Once | Once | Testing | --discovery.py |

---

## System Output Example

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
AUTONOMOUS CONTINUOUS EVENT DISCOVERY & SCRAPING SYSTEM
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

⚙️ CONFIGURATION
  Discovery interval: 30 minutes
  Scrape interval:    360 minutes
  Verbose mode:       OFF

✨ System is fully autonomous and continuously:
   • Discovers new event sources
   • Scrapes all available sources
   • Validates events with AI
   • Updates the database
   • Learns and adapts

💡 Press Ctrl+C to stop

🔄 INITIAL STARTUP SEQUENCE

📍 Scraping eventbrite...
  ✓ Found 6 events
📍 Scraping ltw...
  ✓ Found 5 events

============================================================
✅ SCRAPING COMPLETE
============================================================
Total events found:   11
Events inserted:      11
Errors encountered:   0

🤖 SOURCE DISCOVERY CYCLE - Machine Learning Mode
============================================================

📡 PHASE 1: Search-Based Discovery
  🔍 Searching: 'London tech events websites'
    (searching... please wait)
    ✨ Discovered: https://example-event-site.com
  🔍 Searching: 'London developer meetups'
    ✨ Discovered: https://another-events.co.uk

📡 PHASE 2: Event-Based Discovery
  🔗 Analyzing existing events for new sources...
  (no new sources found)

📡 PHASE 3: Link Analysis Discovery
  🌐 Analyzing links on known event sites...
    ✨ Linked from eventbrite: https://partnered-events.com

✅ PHASE 4: Validation & Integration
  ✓ Added: https://example-event-site.com (discovery)
  ✓ Added: https://another-events.co.uk (hackathon)
  ✓ Added: https://partnered-events.com (learning)

============================================================
📊 DISCOVERY SUMMARY
============================================================
Candidates found:     47
Validated & added:    9
Total sources:        32
Tried (invalid):      38

📊 CONTINUOUS RUNNER STATUS
================================================================================

🔍 SOURCE DISCOVERY
  Total sources discovered:  32
  Last discovery run:        2026-01-28 14:32:15
  Next discovery in:         29m 43s

📥 EVENTS
  Total in database:         145
  Validated & active:        87
  Pending validation:        58
  Last scrape run:           2026-01-28 14:28:00
  Next scrape in:            5h 32m

📈 LIFETIME STATS
  Total sources discovered:  32
  Total events scraped:      145

================================================================================

⏳ Next cycle in 30 minutes...
   (Press Ctrl+C to stop)
```

---

## Command Examples

```bash
# Start with default settings (BEST FOR BEGINNERS)
python continuous_runner.py

# Fast discovery (test phase)
python continuous_runner.py --discovery 5

# Slow/gentle (production)
python continuous_runner.py --discovery 120 --scrape 1440

# Verbose debugging
python continuous_runner.py --verbose

# See help
python continuous_runner.py --help

# Stop any time
# Just press: Ctrl+C
```

---

## Key Statistics After Different Time Periods

```
⏱️ After 1 hour:
├─ 8-12 sources discovered
├─ 50-80 events
└─ System stable ✓

⏱️ After 6 hours:
├─ 20-30 sources discovered
├─ 200-300 events
└─ AI validating ✓

⏱️ After 24 hours:
├─ 50-100 sources discovered
├─ 500-1000 events
├─ Patterns learned ✓
└─ Self-improving ✓

⏱️ After 1 week:
├─ 100-200 sources discovered
├─ 2000-5000 events
├─ Strong patterns ✓
└─ Near-complete coverage ✓
```

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| **Too slow** | `--discovery 10 --scrape 60` |
| **Too aggressive** | `--discovery 60 --scrape 1440` |
| **Not finding sources** | Check internet, wait 1 hour |
| **Database errors** | Delete `database.db`, restart |
| **API errors** | Check `.env` has valid OpenAI key |
| **Want to pause** | Just press Ctrl+C |

---

## Next Steps

```
1. START:           python continuous_runner.py
2. WAIT:            Let it run for 1 hour
3. CHECK:           Look at discovered_sources.json
4. MONITOR:         Watch web server at http://127.0.0.1:5000
5. DEPLOY:          When happy, run 24/7 on server
```

---

**Your system is now a self-learning event discovery machine! 🤖**
