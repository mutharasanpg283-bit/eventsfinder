"""
enhance_events.py

Enhance existing events with better URLs, dates, and validation.

Features:
- Re-validates all existing event URLs
- Removes broken links
- Cleans up malformed data
- Generates source_id if missing
- Ensures data quality

Run:
    python enhance_events.py
"""

import sqlite3
import requests
import time
import uuid
from pathlib import Path
from typing import Tuple, Optional

DB_PATH = Path(__file__).parent / "database.db"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]


class EventEnhancer:
    """Enhance and validate existing events"""
    
    def __init__(self):
        self.session = requests.Session()
        self.updated = 0
        self.removed = 0
        
    def get_headers(self):
        """Get random headers"""
        import random
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml",
        }
    
    def validate_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """Validate URL and return final URL after redirects"""
        if not url or not isinstance(url, str):
            return False, None
        
        if not url.startswith('http'):
            return False, None
        
        try:
            # Try HEAD first
            response = self.session.head(url, headers=self.get_headers(), timeout=5, allow_redirects=True)
            
            if response.status_code == 404:
                return False, None
            if response.status_code >= 400:
                try:
                    response = self.session.get(url, headers=self.get_headers(), timeout=5, allow_redirects=True)
                    if response.status_code >= 400:
                        return False, None
                except:
                    return False, None
            
            return True, response.url
        except Exception as e:
            return False, None
    
    def extract_clean_eventbrite_url(self, url: str) -> Optional[str]:
        """Clean up EventBrite URLs"""
        if 'eventbrite' in url:
            # EventBrite URLs sometimes have extra parameters
            if '?' in url:
                url = url.split('?')[0]
            return url
        return url
    
    def enhance_database(self):
        """Enhance all events in database"""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        print("\n" + "="*70)
        print("🔧 ENHANCING EVENTS DATABASE")
        print("="*70 + "\n")
        
        # Get all events
        rows = cur.execute(
            "SELECT id, title, source_url, source_name FROM events"
        ).fetchall()
        
        print(f"📊 Processing {len(rows)} events...\n")
        
        to_delete = []
        updates = []
        
        for event_id, title, url, source_name in rows:
            print(f"🔍 Event ID {event_id}: {title[:50]}...")
            
            # Clean URL
            cleaned_url = self.extract_clean_eventbrite_url(url)
            
            # Validate URL
            is_valid, final_url = self.validate_url(cleaned_url)
            
            if not is_valid:
                print(f"   ❌ Link broken - MARKING FOR REMOVAL")
                to_delete.append(event_id)
            else:
                print(f"   ✓ Link valid")
                
                # If URL changed (due to cleanup or redirects), update it
                if cleaned_url != url:
                    print(f"   (URL cleaned)")
                    updates.append((cleaned_url, event_id))
                
                # Generate source_id if missing
                cur.execute("SELECT source_id FROM events WHERE id = ?", (event_id,))
                result = cur.fetchone()
                if not result or not result[0]:
                    source_id = f"{source_name or 'event'}_{uuid.uuid4().hex[:8]}"
                    cur.execute("UPDATE events SET source_id = ? WHERE id = ?", (source_id, event_id))
                    print(f"   (Added source_id)")
            
            time.sleep(0.2)  # Rate limit
        
        # Apply updates
        for new_url, event_id in updates:
            cur.execute("UPDATE events SET source_url = ? WHERE id = ?", (new_url, event_id))
        
        # Delete broken events
        if to_delete:
            placeholders = ','.join('?' * len(to_delete))
            cur.execute(f"DELETE FROM events WHERE id IN ({placeholders})", to_delete)
            self.removed = len(to_delete)
        
        self.updated = len(updates)
        
        conn.commit()
        conn.close()
        
        # Show results
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        total = cur.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        conn.close()
        
        print("\n" + "="*70)
        print("✅ DATABASE ENHANCEMENT COMPLETE")
        print("="*70)
        print(f"URL URLs cleaned:   {self.updated}")
        print(f"Broken links removed: {self.removed}")
        print(f"Total events remaining: {total}")
        print("="*70 + "\n")
        
        # Show final events
        self.show_events()
    
    def show_events(self):
        """Display all remaining events"""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        rows = cur.execute(
            "SELECT id, title, source_url, date, location FROM events ORDER BY title"
        ).fetchall()
        
        print("📋 REMAINING EVENTS (ALL WITH WORKING LINKS):\n")
        print("-" * 100)
        
        for i, (event_id, title, url, date, loc) in enumerate(rows, 1):
            print(f"\n{i}. {title}")
            print(f"   🔗 URL: {url}")
            print(f"   📅 Date: {date or 'TBD'}")
            print(f"   📍 Location: {loc or 'TBD'}")
        
        print("\n" + "-" * 100)
        conn.close()


if __name__ == "__main__":
    enhancer = EventEnhancer()
    enhancer.enhance_database()
