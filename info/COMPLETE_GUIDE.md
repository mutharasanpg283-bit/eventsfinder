# Complete Automation & Deployment Guide

## Executive Summary

You now have **multiple ways to run your app** - from clicking a button to cloud deployment. Choose based on your needs.

---

# Part 1: How to Run It Now (3 Ways)

## Way 1: Double-Click (Windows Only)

**File:** `run.bat`

**How:**
1. Open File Explorer
2. Go to your project folder
3. Double-click `run.bat`
4. Done! PowerShell opens and runs everything

**What happens:**
- ✅ Activates virtual environment
- ✅ Runs full workflow automatically
- ✅ Browser opens to web interface
- ✅ Press Ctrl+C to stop

---

## Way 2: Command Line (All Platforms)

**Basic (full workflow):**
```bash
python main.py
```

**What it does:**
1. Scrapes events from Eventbrite
2. Validates with AI
3. Starts web server
4. You can visit http://127.0.0.1:5000

**Single operations:**
```bash
python main.py --scrape-only       # Just fetch events
python main.py --validate-only     # Just validate events  
python main.py --serve-only        # Just start web server
```

---

## Way 3: Continuous Background Running

**Run with auto-updates:**
```bash
python main.py --schedule 24
```

**What it does:**
- Starts web server
- Runs scraper every 24 hours
- Validates events after each scrape
- Keeps running until you press Ctrl+C

**Custom schedules:**
```bash
python main.py --schedule 1        # Update every 1 hour
python main.py --schedule 12       # Update every 12 hours
python main.py --schedule 168      # Update weekly (168 hours)
```

---

# Part 2: Automation Options

## Option A: Manual (No Automation)

**Use when:** You want full control, one-off runs

```bash
# Whenever you want:
python main.py
```

**Pros:** Simple, understand what's running
**Cons:** Must remember to run it

---

## Option B: Windows Task Scheduler (Automatic on Schedule)

**Use when:** You want daily automatic updates

**Setup (5 minutes):**

1. Create file `update-only.bat` in project folder:
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py --scrape-only
python main.py --validate-only
```

2. Open Task Scheduler:
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

3. Click **Create Task**

4. **General tab:**
   - Name: `Event Finder Daily Update`

5. **Triggers tab:**
   - Click **New**
   - Choose **Daily**
   - Set time: `8:00 AM`
   - Click OK

6. **Actions tab:**
   - Click **New**
   - Program: `C:\Users\mutha\Desktop\event\update-only.bat`
   - Start in: `C:\Users\mutha\Desktop\event`
   - Click OK

7. **OK**

**What happens:**
- Every day at 8:00 AM, your events update automatically
- No human intervention needed
- Silent operation (no window)

**Cost:** Free

---

## Option C: Always-Running Service (Linux/Mac/VPS)

**Use when:** You want a server always online

### On Linux with systemd:

**Create `/etc/systemd/system/event-finder.service`:**
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

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable event-finder
sudo systemctl start event-finder
```

**Check status:**
```bash
sudo systemctl status event-finder
```

---

## Option D: Docker Container (Portable/Cloud)

**Use when:** You want to deploy anywhere

**Create `Dockerfile`:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
CMD ["python", "main.py", "--schedule", "24"]
```

**Build:**
```bash
docker build -t event-finder .
```

**Run locally:**
```bash
docker run -e OPENAI_API_KEY="sk-..." event-finder
```

**Push to Docker Hub:**
```bash
docker tag event-finder yourusername/event-finder
docker push yourusername/event-finder
```

**Deploy anywhere that runs Docker**

---

# Part 3: Deployment Strategies

## Strategy 1: Local PC (What You Have Now)

**For:** Personal use, development

```
Your Computer
    ↓
[main.py]
    ↓
http://127.0.0.1:5000 (only on your PC)
```

**Cost:** $0 (besides OpenAI API)
**Complexity:** Simple (just run `python main.py`)
**Uptime:** When your PC is on
**Users:** Just you

---

## Strategy 2: VPS Server (Best for Small Product)

**For:** Small product, ~10-100 daily users

**Setup:**
1. Rent VPS ($5-10/month from DigitalOcean, Linode, Vultr)
2. Install Python and dependencies
3. Setup systemd service (see above)
4. Setup nginx reverse proxy (handles HTTPS, caching)
5. Enable HTTPS with Let's Encrypt (free)

```
Domain yourdomain.com
    ↓
  Nginx (reverse proxy + HTTPS)
    ↓
[main.py] on VPS
    ↓
[PostgreSQL] database (reliability)
```

**Cost:** $50-100/month
**Complexity:** Medium (one-time setup)
**Uptime:** 99.9% (professional hosting)
**Users:** 10-100s of concurrent

---

## Strategy 3: Docker on Cloud (Scalable)

**For:** Rapid scaling, multiple regions

**Platforms:**
- Render.com (easiest, free tier)
- Railway.app (modern, good free tier)
- Heroku (industry standard)
- AWS ECS (professional)
- Google Cloud Run (serverless)

**Deployment:**
```bash
# Example with Render
1. Push code to GitHub
2. Connect GitHub to Render
3. Deploy from Docker
4. Done!
```

```
Render.com / Railway
    ↓
[Docker Container]
    ↓
Auto-scaling, 99.99% uptime
```

**Cost:** $7-50/month (depending on traffic)
**Complexity:** Easy (connect GitHub)
**Uptime:** 99.99% (built-in)
**Users:** 100s to 1000s

---

## Strategy 4: Kubernetes (Enterprise)

**For:** Large-scale product, millions of users

```
Load Balancer
    ↓
├─ [main.py] pod
├─ [main.py] pod
├─ [main.py] pod (auto-scaled)
    ↓
├─ [PostgreSQL] master
├─ [PostgreSQL] replicas (backup)
    ↓
├─ Redis (caching)
├─ ElasticSearch (search)
    ↓
CDN (content distribution)
```

**Providers:**
- AWS EKS
- Google GKE
- Azure AKS
- DigitalOcean Kubernetes

**Cost:** $100-1000+/month
**Complexity:** High (DevOps needed)
**Uptime:** 99.999%
**Users:** Millions

---

# Part 4: Step-by-Step for Each Scenario

## Scenario 1: Just You, Daily Use

```bash
# Every morning:
python main.py

# Done! Use the web app
```

**Time investment:** 2 minutes per day

---

## Scenario 2: You + Automated Updates

```bash
# Setup Windows Task Scheduler (once, 10 minutes)
# Then never think about it again

# Visit: http://127.0.0.1:5000 anytime
```

**Time investment:** 10 minutes one-time setup

---

## Scenario 3: Small Team (~10 people)

**Setup once:**
```bash
# 1. Rent VPS ($10/month)
# 2. SSH into server
ssh user@your-vps.com

# 3. Clone your code
git clone https://github.com/yourusername/event-finder.git
cd event-finder

# 4. Setup Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Create systemd service (see above)

# 6. Setup nginx + HTTPS (Let's Encrypt)

# That's it! Now available at yourdomain.com
```

**Time investment:** 1-2 hours one-time
**Monthly cost:** $20-50
**Now available:** To anyone on the internet 24/7

---

## Scenario 4: Real Product (MVP)

**Technology:**
- VPS + Docker (DigitalOcean App Platform)
- PostgreSQL database
- Redis cache
- Nginx + Cloudflare CDN

**Setup:**
```bash
# 1. Create Dockerfile
# 2. Push to GitHub
# 3. Connect DigitalOcean App Platform
# 4. Deploy with 1 click
# 5. Auto-scales based on traffic
```

**Cost:** $12-50/month
**Uptime:** 99.9%
**Performance:** Global CDN caching
**Monitoring:** Built-in analytics
**Time:** ~2 hours setup

---

## Scenario 5: Enterprise (Scaling)

**Professional setup:**
- Kubernetes cluster
- Multiple regions
- 24/7 monitoring
- Auto-scaling
- Advanced caching
- Load balancing

**Cost:** $500-5000+/month
**Uptime:** 99.99%
**Capacity:** Millions of users
**Time:** Needs DevOps team

---

# Part 5: Recommended Path

### If you're just learning:
**Start with:** `python main.py` (manual runs)

### If you're using daily:
**Upgrade to:** Windows Task Scheduler (automatic daily)

### If you want to share with friends:
**Upgrade to:** VPS (DigitalOcean, $10/month)

### If it becomes popular:
**Upgrade to:** Docker on Render/Railway (auto-scaling)

### If it's a real business:
**Upgrade to:** Kubernetes (enterprise-grade)

---

# Part 6: Quick Migration Guide

**From Manual → Automated:**
```bash
# Step 1: Install to production (VPS, Docker, etc.)
# Step 2: Change ONE LINE in main.py to use production database
# Step 3: Change host from 127.0.0.1 to 0.0.0.0 in server.py
# That's it!
```

All your code works everywhere - it's designed for it!

---

# Summary Table

| Need | Solution | Cost | Time | Users |
|------|----------|------|------|-------|
| Personal dev | `python main.py` | Free | 2 min | 1 |
| Auto updates | Task Scheduler | Free | 10 min | 1 |
| Team sharing | VPS + Nginx | $20/mo | 2 hrs | 10s |
| Product MVP | Docker + Render | $20/mo | 1 hr | 100s |
| Scaling | Kubernetes | $500+/mo | 1 week | 1000s+ |

---

**Your project is ready for ANY of these paths! The code doesn't need to change - just the infrastructure changes.**

Choose based on your current needs, upgrade later when you're ready. 🚀
