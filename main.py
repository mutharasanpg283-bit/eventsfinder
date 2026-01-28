#!/usr/bin/env python3
"""
main.py - Orchestrator for London Tech Events Finder

This is the single entry point for the entire application.
It handles scraping, AI validation, and web server automatically.

Usage:
    python main.py                    # Full workflow (scrape + validate + serve)
    python main.py --scrape-only      # Just fetch events
    python main.py --validate-only    # Just validate events
    python main.py --serve-only       # Just start web server
    python main.py --schedule         # Run scraper on a schedule
    python main.py --help             # Show all options
"""

import sys
import os
import argparse
import time
import subprocess
from pathlib import Path
from datetime import datetime
import signal

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EventFinder:
    """Main orchestrator class"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    def check_api_key(self):
        """Verify API key is set"""
        if not self.api_key:
            print("\n[FAIL] ERROR: OPENAI_API_KEY not found in .env")
            print("   Please set your API key: https://platform.openai.com/api-keys")
            return False
        return True
    
    def run_scraper(self):
        """Run the scraper (uses advanced multi-source scraper)"""
        print("\n" + "="*60)
        print("[SCRAPE] STEP 1: Scraping Events from 46+ Sources")
        print("="*60)
        
        try:
            # Import and run advanced scraper
            import scraper_advanced
            scraper_advanced.scrape_london_tech_events()
            print("\n[OK] Scraping completed successfully!")
            return True
        except Exception as e:
            print(f"\n[ERROR] Scraping failed: {e}")
            return False
    
    def remove_duplicates(self):
        """Remove duplicate events from database"""
        print("\n" + "="*60)
        print(">> Removing Duplicate Events")
        print("="*60)
        
        try:
            import sqlite3
            conn = sqlite3.connect(self.project_root / "database.db")
            cur = conn.cursor()
            
            # Find duplicates: same title, location, and date
            duplicates = cur.execute("""
                SELECT id, title FROM events 
                WHERE id NOT IN (
                    SELECT MIN(id) FROM events 
                    GROUP BY LOWER(TRIM(title)), LOWER(TRIM(location)), date
                )
                ORDER BY id DESC
            """).fetchall()
            
            if duplicates:
                dup_count = len(duplicates)
                dup_ids = [str(row[0]) for row in duplicates]
                print(f"\n[Found] {dup_count} duplicate events\n")
                
                for event_id, title in duplicates:
                    print(f"  [DELETE] Removing duplicate: {title[:50]}...")
                
                # Delete duplicates
                cur.execute(f"DELETE FROM events WHERE id IN ({','.join(dup_ids)})")
                conn.commit()
                print(f"\n[OK] Removed {dup_count} duplicate events")
            else:
                print("\n[OK] No duplicates found")
            
            conn.close()
            return True
        except Exception as e:
            print(f"\n[ERROR] Duplicate removal failed: {e}")
            return False
    
    def clean_broken_urls(self):
        """Remove events with broken/relative URLs"""
        print("\n" + "="*60)
        print(">> Cleaning Broken URLs")
        print("="*60)
        
        try:
            import sqlite3
            conn = sqlite3.connect(self.project_root / "database.db")
            cur = conn.cursor()
            
            # Remove relative URLs (starting with /)
            bad_urls = cur.execute("SELECT id, title FROM events WHERE source_url LIKE '/%'").fetchall()
            
            if bad_urls:
                bad_count = len(bad_urls)
                bad_ids = [str(row[0]) for row in bad_urls]
                print(f"\n[Found] {bad_count} events with broken relative URLs\n")
                
                for event_id, title in bad_urls[:10]:  # Show first 10
                    print(f"  [DELETE] Removing: {title[:50]}...")
                
                if bad_count > 10:
                    print(f"  ... and {bad_count - 10} more")
                
                # Delete them
                cur.execute(f"DELETE FROM events WHERE id IN ({','.join(bad_ids)})")
                conn.commit()
                print(f"\n[OK] Removed {bad_count} events with broken URLs")
            else:
                print("\n[OK] No broken relative URLs found")
            
            conn.close()
            return True
        except Exception as e:
            print(f"\n[ERROR] URL cleaning failed: {e}")
            return False
    
    def validate_event_urls(self):
        """Validate that event URLs actually work"""
        print("\n" + "="*60)
        print(">> Validating Event URL Accessibility")
        print("="*60)
        
        try:
            # Import and run link validator
            import link_validator
            validator = link_validator.LinkValidator()
            validator.clean_database()
            print("\n[OK] URL validation completed!")
            return True
        except Exception as e:
            print(f"\n[WARN] URL validation skipped: {e}")
            # Don't fail the entire pipeline for this
            return True
    
    def enhance_event_data(self):
        """Enhance events with better data and remove invalid ones"""
        print("\n" + "="*60)
        print(">> Enhancing Event Data Quality")
        print("="*60)
        
        try:
            # Import and run event enhancer
            import enhance_events
            enhancer = enhance_events.EventEnhancer()
            enhancer.enhance_database()
            print("\n[OK] Event enhancement completed!")
            return True
        except Exception as e:
            print(f"\n[WARN] Event enhancement skipped: {e}")
            # Don't fail the entire pipeline for this
            return True
    
    def run_ai_cleaner(self):
        """Run AI validation"""
        print("\n" + "="*60)
        print("[AI] STEP 2: AI Validation & Categorization")
        print("="*60)
        
        try:
            # Import and run AI cleaner
            import ai_cleaner
            ai_cleaner.main()
            print("\n[OK] AI validation completed successfully!")
            return True
        except Exception as e:
            print(f"\n[ERROR] AI validation failed: {e}")
            return False
    
    def run_server(self):
        """Run the Flask server"""
        print("\n" + "="*60)
        print("[SERVER] STEP 3: Starting Web Server")
        print("="*60)
        print("\n[OK] Web server starting at http://127.0.0.1:5000")
        print("  Open your browser and visit the URL above")
        print("  Press Ctrl+C to stop the server")
        print("="*60 + "\n")
        
        try:
            import server
            # Run the server (this blocks until Ctrl+C)
            server.app.run(host="127.0.0.1", port=5000, debug=True)
        except KeyboardInterrupt:
            print("\n\n[OK] Server stopped by user")
            return True
        except Exception as e:
            print(f"\n[ERROR] Server failed: {e}")
            return False
    
    def run_full_workflow(self):
        """Run complete workflow: scrape -> clean -> enhance -> validate -> serve"""
        print("\n[START] LONDON TECH EVENTS FINDER - FULL WORKFLOW")
        print("   Scraping → Cleaning → Enhancing → Validating → Serving")
        
        # Step 1: Scrape
        if not self.run_scraper():
            print("\n[WARN]  Scraping failed, but continuing with existing data...")
        
        # Step 2: Remove duplicates
        if not self.remove_duplicates():
            print("\n[WARN]  Duplicate removal failed, continuing...")
        
        # Step 3: Clean broken URLs
        if not self.clean_broken_urls():
            print("\n[WARN]  URL cleaning failed, continuing...")
        
        # Step 4: Validate event URLs
        if not self.validate_event_urls():
            print("\n[WARN]  URL validation failed, continuing...")
        
        # Step 5: Enhance event data
        if not self.enhance_event_data():
            print("\n[WARN]  Event enhancement failed, continuing...")
        
        # Step 6: Validate with AI
        if not self.run_ai_cleaner():
            print("\n[WARN]  AI validation failed, but continuing...")
        
        # Step 7: Serve
        self.run_server()
    
    def run_scheduled(self, interval_hours=24):
        """Run scraper and validator on schedule, keep server running"""
        print(f"\n[SCHEDULE] SCHEDULED MODE - Updates every {interval_hours} hours")
        print("   Server will run continuously")
        print("   Press Ctrl+C to stop\n")
        
        last_run = 0
        
        def scrape_and_validate():
            """Helper to run complete data pipeline"""
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running scheduled update...")
            self.run_scraper()
            self.remove_duplicates()
            self.clean_broken_urls()
            self.validate_event_urls()
            self.enhance_event_data()
            self.run_ai_cleaner()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Update complete!")
        
        try:
            # Initial run
            scrape_and_validate()
            
            # Start server in background and handle scheduling
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting web server...")
            import server
            from threading import Thread
            
            # Run server in background thread
            server_thread = Thread(target=lambda: server.app.run(
                host="127.0.0.1", port=5000, debug=False, use_reloader=False
            ), daemon=True)
            server_thread.start()
            
            print("[OK] Web server running at http://127.0.0.1:5000")
            print("  Scheduled updates active\n")
            
            # Keep running and check schedule
            interval_seconds = interval_hours * 3600
            last_run = time.time()
            
            while True:
                time.sleep(60)  # Check every minute
                current_time = time.time()
                
                if current_time - last_run >= interval_seconds:
                    scrape_and_validate()
                    last_run = current_time
        
        except KeyboardInterrupt:
            print("\n\n[OK] Scheduler stopped by user")
        except Exception as e:
            print(f"\n[ERROR] Scheduled mode failed: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="London Tech Events Finder - Automated Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                   # Full workflow (scrape → clean → enhance → validate → serve)
  python main.py --serve-only      # Start web server only
  python main.py --scrape-only     # Fetch new events
  python main.py --clean-only      # Remove duplicates and broken links
  python main.py --validate-only   # Run AI validation only
  python main.py --schedule 24     # Update every 24 hours, serve continuously
        """
    )
    
    parser.add_argument(
        "--scrape-only",
        action="store_true",
        help="Run only the scraper"
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Run data cleaning pipeline (remove duplicates, broken URLs, validate, enhance)"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Run only AI validation"
    )
    parser.add_argument(
        "--serve-only",
        action="store_true",
        help="Run only the web server"
    )
    parser.add_argument(
        "--schedule",
        type=int,
        metavar="HOURS",
        help="Run scraper and validator on schedule (every N hours) with continuous server"
    )
    
    args = parser.parse_args()
    
    # Create orchestrator
    finder = EventFinder()
    
    # Check API key if needed
    if not args.serve_only and not args.clean_only and not finder.check_api_key():
        sys.exit(1)
    
    # Execute requested action
    try:
        if args.schedule:
            finder.run_scheduled(args.schedule)
        elif args.scrape_only:
            finder.run_scraper()
        elif args.clean_only:
            finder.remove_duplicates()
            finder.clean_broken_urls()
            finder.validate_event_urls()
            finder.enhance_event_data()
            print("\n[OK] Cleaning pipeline completed!")
        elif args.validate_only:
            finder.run_ai_cleaner()
        elif args.serve_only:
            finder.run_server()
        else:
            # Default: full workflow
            finder.run_full_workflow()
    
    except KeyboardInterrupt:
        print("\n\n[OK] Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
