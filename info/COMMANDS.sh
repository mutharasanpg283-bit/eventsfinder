#!/bin/bash
# Quick Reference - Common Commands

# ============================================
# FULL AUTOMATED WORKFLOW
# ============================================
python main.py
# Runs: Scrape → Clean → Enhance → Validate → Serve
# Best for: Initial setup or periodic full updates
# Duration: ~1-2 hours


# ============================================
# JUST START THE WEB SERVER
# ============================================
python main.py --serve-only
# Serves existing data without scraping
# Best for: Running the app with existing data
# Duration: Starts immediately


# ============================================
# CLEAN EXISTING DATA
# ============================================
python main.py --clean-only
# Removes duplicates, broken links, enhances data
# Best for: Improving data quality without scraping
# Duration: ~20-30 minutes


# ============================================
# SCRAPE ONLY
# ============================================
python main.py --scrape-only
# Fetches new events from 46+ sources
# Best for: Getting fresh data
# Duration: ~10-15 minutes


# ============================================
# AI VALIDATION ONLY
# ============================================
python main.py --validate-only
# Validates pending events with OpenAI
# Best for: Processing unvalidated events
# Duration: ~30-60 minutes


# ============================================
# SCHEDULED MODE (RECOMMENDED)
# ============================================
python main.py --schedule 24
# Updates every 24 hours, serves continuously
# Best for: Production (automatic daily updates)
# Duration: Runs indefinitely


# ============================================
# QUICK VALIDATION
# ============================================
# Check if there are issues with data
python main.py --help
# Shows all available options


# ============================================
# DEVELOPMENT WORKFLOW
# ============================================

# 1. Start fresh
python main.py

# 2. Visit http://127.0.0.1:5000/

# 3. Review in admin panel at http://127.0.0.1:5000/admin
#    Login: admin / events2026

# 4. For next update
python main.py --schedule 24  # Or just run full pipeline again


# ============================================
# TROUBLESHOOTING
# ============================================

# Missing API key?
# Create .env file:
# echo "OPENAI_API_KEY=sk-..." > .env

# Port 5000 already in use?
# Kill process: pkill -f "python server.py"
# Or modify server.py to use different port

# Data issues?
# Clean with: python main.py --clean-only
# Then validate: python main.py --validate-only

# Want to see what would be deleted?
# Check database before/after with:
# python -c "import sqlite3; c=sqlite3.connect('database.db').cursor(); print('Total:', c.execute('SELECT COUNT(*) FROM events').fetchone()[0])"


# ============================================
# PRODUCTION SETUP (Linux/Windows)
# ============================================

# Option 1: Background process
nohup python main.py --schedule 24 > event_runner.log 2>&1 &

# Option 2: Systemd service (Linux)
# Create /etc/systemd/system/events.service with:
# [Unit]
# Description=London Tech Events Finder
# After=network.target
#
# [Service]
# Type=simple
# User=events
# WorkingDirectory=/opt/events
# ExecStart=/usr/bin/python3 main.py --schedule 24
# Restart=always
#
# [Install]
# WantedBy=multi-user.target

# Then enable:
# sudo systemctl enable events
# sudo systemctl start events
# sudo systemctl status events

# Option 3: Windows Task Scheduler
# 1. Create bat file: run_events.bat
#    @echo off
#    cd C:\Users\mutha\Desktop\event
#    python main.py --schedule 24
#
# 2. Create scheduled task to run run_events.bat at startup


# ============================================
# MONITORING
# ============================================

# Check running process
ps aux | grep main.py

# View logs
tail -f event_runner.log

# Check database size
du -h database.db

# Count events
sqlite3 database.db "SELECT COUNT(*) FROM events;"

# See valid events
sqlite3 database.db "SELECT COUNT(*) FROM events WHERE is_valid=1;"


# ============================================
# API EXAMPLES
# ============================================

# Get all events
curl http://127.0.0.1:5000/api/events

# Get pretty JSON
curl http://127.0.0.1:5000/api/events | python -m json.tool

# Delete event (requires admin auth)
curl -X DELETE http://127.0.0.1:5000/api/events/1


# ============================================
# MAINTENANCE
# ============================================

# Backup database
cp database.db database.db.backup

# Reset database (WARNING: deletes all data)
rm database.db
python main.py  # Will recreate empty database

# Clear cache
rm -rf __pycache__

# Install updates
pip install -r requirements.txt --upgrade
