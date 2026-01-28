# QUICK REFERENCE - How to Run Everything

## 🚀 Easiest Way (Windows)

**Double-click this file:**
```
run.bat
```

Done! Everything runs automatically. Browser opens to http://127.0.0.1:5000

---

## 💻 Command Line Ways

### **Full workflow (Scrape → Validate → Serve)**
```bash
python main.py
```

### **Just fetch events**
```bash
python main.py --scrape-only
```

### **Just validate events**
```bash
python main.py --validate-only
```

### **Just start web server**
```bash
python main.py --serve-only
```

### **Auto-update every 24 hours + serve**
```bash
python main.py --schedule 24
```

### **Auto-update every 12 hours + serve**
```bash
python main.py --schedule 12
```

### **Auto-update every hour + serve**
```bash
python main.py --schedule 1
```

---

## 🎯 Recommended Setups

### Setup 1: Desktop User (You)
```bash
# Run manually whenever you want:
python main.py
```
- Run every day before using the app
- Takes ~2-3 minutes
- Simplest approach

### Setup 2: Always Running (Background)
```bash
# Keeps running, auto-updates daily:
python main.py --schedule 24
```
- Leave running in PowerShell window
- Automatically updates at intervals
- Best for daily use

### Setup 3: Completely Automatic (Windows)
1. Use Windows Task Scheduler (see DEPLOYMENT.md)
2. Creates scheduled task that runs `update-only.bat` daily
3. Server runs on-demand when you visit the page
4. Zero manual work

### Setup 4: Always-On Server (Production)
See DEPLOYMENT.md for:
- VPS (DigitalOcean, Linode)
- Docker deployment
- Cloud platforms (Heroku, Render, AWS)
- Professional scaling

---

## 🔧 File Structure

```
Your Project:
├── main.py                  ← RUN THIS (new orchestrator)
├── run.bat                  ← OR DOUBLE-CLICK THIS (Windows)
├── run.sh                   ← Or this (Mac/Linux)
├── scraper.py               ← Called by main.py
├── ai_cleaner.py           ← Called by main.py
├── server.py               ← Called by main.py
└── ... (other files)
```

---

## 📊 Workflow Comparison

| What | Time | Manual | Automatic |
|------|------|--------|-----------|
| **Once per day** | ~2-3 min | `python main.py` | Task Scheduler |
| **Every few hours** | ~2-3 min each | Keep running? | `python main.py --schedule 6` |
| **Continuous** | Runs forever | Leave open | Background service |
| **Production** | ∞ uptime | No way | VPS + systemd |

---

## 🎬 Step-by-Step for First Time

1. **Open PowerShell** in your project folder
2. **Run**:
   ```bash
   python main.py
   ```
3. **Wait** for it to finish scraping and validating (~2-3 minutes)
4. **Browser** opens automatically
5. **Enjoy!** Events display at http://127.0.0.1:5000
6. **Press Ctrl+C** to stop

---

## 🔄 For Daily Use

**Morning routine:**
```bash
python main.py
```
This:
- ✅ Fetches new events
- ✅ Validates them with AI
- ✅ Starts web server
- ✅ Opens browser
- ✅ You browse events

---

## ⏰ For Always-Running Setup

**Run once:**
```bash
python main.py --schedule 24
```

Then:
- Leave PowerShell window open
- Events auto-update every 24 hours
- Web server always available
- Visit anytime: http://127.0.0.1:5000

**Stop with:** `Ctrl+C`

---

## 🌐 For Actual Product

See **DEPLOYMENT.md** for:
- Docker deployment
- VPS setup (DigitalOcean, Linode)
- Cloud platforms (Heroku, Render, Railway)
- Database migration (SQLite → PostgreSQL)
- HTTPS & domain setup
- Monitoring & alerts
- Scaling strategies

**TL;DR for product:**
1. Use VPS + Docker
2. Deploy to DigitalOcean/Linode (~$10/month)
3. Add PostgreSQL database
4. Setup Nginx + HTTPS
5. Enable systemd auto-restart
6. Add monitoring (Sentry, Datadog)

---

## 🐛 Troubleshooting

**"Module not found"** → Reinstall: `pip install -r requirements.txt`

**"OPENAI_API_KEY not found"** → Edit .env with your key

**"Port 5000 already in use"** → Use: `python main.py --serve-only --port 5001`

**"Can't find .env"** → Make sure you're in the project folder

---

## ✨ Summary

### **Local desktop:**
```bash
python main.py
```

### **Background (auto-update):**
```bash
python main.py --schedule 24
```

### **Production:**
See DEPLOYMENT.md

That's all you need to know! 🎉
