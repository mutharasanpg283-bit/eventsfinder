# Deployment & Automation Guide

Everything you need to know about running this application - from local desktop to production.

---

## 🎯 Quick Start (Choose Your Method)

### **Option 1: Windows Desktop (Easiest)**
1. Edit `.env` with your OpenAI API key
2. **Double-click `run.bat`**
3. Browser opens to http://127.0.0.1:5000 automatically

### **Option 2: Terminal Command**
```bash
python main.py
```

### **Option 3: Specific Operations**
```bash
python main.py --scrape-only      # Just fetch events
python main.py --validate-only    # Just validate events
python main.py --serve-only       # Just start web server
python main.py --schedule 24      # Auto-update every 24 hours
```

---

## 📊 Available Commands

### **Full Workflow** (Default)
```bash
python main.py
```
Runs: Scraper → AI Validation → Web Server

### **Scraper Only**
```bash
python main.py --scrape-only
```
Fetches ~50 new events, exits after done

### **Validator Only**
```bash
python main.py --validate-only
```
Processes unvalidated events, exits after done

### **Server Only**
```bash
python main.py --serve-only
```
Starts web server, no scraping/validation

### **Scheduled Mode** (Recommended for Always-On)
```bash
python main.py --schedule 24
```
- Runs scraper every 24 hours
- Validator runs after each scrape
- Server runs continuously
- Press Ctrl+C to stop

### **Custom Schedule**
```bash
python main.py --schedule 12      # Update every 12 hours
python main.py --schedule 1       # Update every hour
python main.py --schedule 168     # Update weekly (168 hours)
```

---

## 🖥️ Windows Desktop Usage

### **Method 1: Double-Click (Easiest)**
1. Open File Explorer
2. Navigate to your project folder
3. **Double-click `run.bat`**
4. PowerShell opens and runs everything
5. Browser opens when ready

### **Method 2: Command Line**
```powershell
cd c:\Users\mutha\Desktop\event
python main.py
```

### **Method 3: Create Desktop Shortcut**
1. Right-click `run.bat` → Create Shortcut
2. Move to Desktop
3. Double-click shortcut to run

---

## 🔄 Scheduled Automation (Windows Task Scheduler)

### **Setup Automatic Daily Updates**

1. **Create batch file `update-only.bat`**:
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py --scrape-only
python main.py --validate-only
```

2. **Open Task Scheduler**:
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Click `Create Task`

3. **Configure Task**:
   - **General**: Name = "Event Finder Daily Update"
   - **Triggers**: New → Daily at 8:00 AM
   - **Actions**: New → Start Program
     - Program: `C:\Users\mutha\Desktop\event\update-only.bat`
     - Start in: `C:\Users\mutha\Desktop\event`
   - **OK**

Now your events automatically update every day at 8 AM!

---

## 🐧 Linux / macOS Setup

### **Make Script Executable**
```bash
chmod +x run.sh
```

### **Run Directly**
```bash
./run.sh
```

### **Create Desktop Launcher (Ubuntu)**
1. Create `EventFinder.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=Event Finder
Exec=/home/user/event/run.sh
Path=/home/user/event/
Terminal=true
```

2. Save to: `~/.local/share/applications/`

### **Automated Updates (Linux cron)**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 8 AM):
0 8 * * * cd /home/user/event && source venv/bin/activate && python main.py --scrape-only && python main.py --validate-only
```

### **Automated with Server (systemd)**
Create `/etc/systemd/system/event-finder.service`:
```ini
[Unit]
Description=London Tech Events Finder
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/event
ExecStart=/home/ubuntu/event/venv/bin/python /home/ubuntu/event/main.py --schedule 24
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable event-finder
sudo systemctl start event-finder
sudo systemctl status event-finder
```

---

## 🌐 Production Deployment

For a real product, use one of these approaches:

### **Option A: Heroku/Railway/Render** (Easiest)

**Pros**: One-click deploy, automatic scaling, free tier available
**Cons**: Limited free tier, may incur costs

#### **Render.com Example**:
1. Push code to GitHub
2. Connect GitHub to Render
3. Create Web Service
4. Set environment variables
5. Deploy

**Changes needed**:
- Add `Procfile`:
```
web: python main.py --serve-only
clock: python main.py --schedule 24
```

- Use environment variable for port:
```python
port = int(os.getenv("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```

---

### **Option B: Docker + Cloud** (Professional)

**Pros**: Portable, scalable, industry standard
**Cons**: More complex setup

**Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV FLASK_ENV=production

CMD ["python", "main.py", "--schedule", "24"]
```

**Build and run**:
```bash
docker build -t event-finder .
docker run -e OPENAI_API_KEY="sk-..." event-finder
```

Deploy to:
- **Docker Hub** → Deploy anywhere
- **AWS ECS** → Managed containers
- **Kubernetes** → Enterprise-scale

---

### **Option C: AWS EC2** (Full Control)

**Pros**: Full control, competitive pricing
**Cons**: Manual setup and maintenance

1. Launch Ubuntu EC2 instance
2. Install Python and dependencies
3. Clone your code
4. Run `python main.py --schedule 24`
5. Use systemd (see Linux section above)

---

### **Option D: VPS** (Best for Small Product)

**Providers**: DigitalOcean, Linode, Vultr ($5-10/month)

**Setup**:
1. SSH into server
2. Install dependencies
3. Clone code
4. Setup systemd service (see above)
5. Setup nginx reverse proxy
6. Enable HTTPS with Let's Encrypt

**Nginx config** (`/etc/nginx/sites-available/events`):
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }
}
```

---

## 🔐 Production Recommendations

| Aspect | Local Dev | Production |
|--------|-----------|-----------|
| **Hosting** | Your PC | Cloud (VPS/Docker/Managed) |
| **Database** | SQLite | PostgreSQL or MySQL |
| **API** | OpenAI (paid) | OpenAI + Rate limiting |
| **HTTPS** | No | Yes (Let's Encrypt) |
| **Auth** | None | Add user login |
| **Monitoring** | Manual | Uptime monitoring |
| **Scaling** | N/A | Load balancer |
| **Updates** | Manual | Automated CI/CD |

---

## 📈 Scaling Path as Product Grows

### **Stage 1: MVP (Now)**
- Local SQLite database
- Single server
- Manual updates
- **Cost**: $0 (free tier OpenAI)

### **Stage 2: Small Scale**
- VPS ($10-20/month)
- PostgreSQL database
- Automated updates via cron
- Basic monitoring
- **Cost**: ~$20/month

### **Stage 3: Growing**
- Multiple servers with load balancer
- Redis for caching
- Separate scraper worker processes
- User authentication
- Analytics dashboard
- **Cost**: ~$100-500/month

### **Stage 4: Enterprise**
- Kubernetes cluster
- Multiple microservices
- CDN for static files
- Advanced caching
- 24/7 monitoring & alerts
- **Cost**: $500+/month

---

## 🚀 Best Production Setup (Recommended)

**For a real product, I recommend:**

```
Digital Ocean VPS ($5-10/month) + Cloudflare ($20-200/month)
                        ↓
                  Linux Server
                        ↓
              Systemd Service (auto-restart)
                        ↓
              Python App (main.py --schedule 24)
                        ↓
          Nginx Reverse Proxy (caching, HTTPS)
                        ↓
           PostgreSQL Database (reliability)
                        ↓
         Cloudflare CDN (speed, DDoS protection)
```

**Why this setup:**
- ✅ Reliable
- ✅ Affordable ($50-100/month)
- ✅ Scalable
- ✅ Simple to manage
- ✅ Industry standard

---

## 📊 Monitoring & Logging

### **Local Logging**
```python
# Add to main.py
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### **Production Monitoring**
Use services like:
- **Sentry** - Error tracking
- **Datadog** - Full stack monitoring
- **UptimeRobot** - Uptime alerts
- **CloudWatch** - AWS monitoring
- **New Relic** - Application performance

---

## 💡 Common Issues & Solutions

### **Port Already in Use**
```bash
python main.py --serve-only --port 5001
```

### **API Key Not Found**
Make sure `.env` has your key:
```bash
cat .env | grep OPENAI_API_KEY
```

### **Server Crashes on Startup**
Check logs:
```bash
tail -f app.log
```

### **Database Locked (SQLite)**
SQLite doesn't handle concurrent writes well. For production:
- Migrate to PostgreSQL
- Or increase WAL timeout

---

## 🎯 Summary: Run It Now

**Quickest way to get running:**

### Windows:
```bash
python main.py
```

### Scheduled (24 hour updates):
```bash
python main.py --schedule 24
```

### Just web server:
```bash
python main.py --serve-only
```

---

**That's it! The `main.py` orchestrator handles everything.**

For questions, see START_HERE.md or README.md.
