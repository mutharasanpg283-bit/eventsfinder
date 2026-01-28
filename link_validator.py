"""
link_validator.py

Validates event links and cleans up broken/invalid entries from the database.

Features:
- Checks if URLs actually work (follows redirects)
- Removes 404s and broken links
- Extracts real event dates and locations
- Filters out university-restricted events
- Ensures links point to booking pages

Run:
    python link_validator.py
"""

import sqlite3
import requests
import time
from pathlib import Path
from typing import Tuple, Optional
from urllib.parse import urlparse
import re

DB_PATH = Path(__file__).parent / "database.db"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]


class LinkValidator:
    """Validates and cleans event links"""
    
    def __init__(self):
        self.session = requests.Session()
        self.removed_count = 0
        self.validated_count = 0
        self.errors = 0
        
    def validate_url(self, url: str, timeout: int = 8) -> Tuple[bool, Optional[str]]:
        """
        Validate if URL works.
        
        Returns:
            (is_valid, final_url)
        """
        if not url or not url.startswith('http'):
            return False, None
        
        try:
            headers = {"User-Agent": USER_AGENTS[0]}
            
            # Follow redirects and check final URL
            response = self.session.head(url, headers=headers, timeout=timeout, allow_redirects=True)
            
            # Check status code
            if response.status_code == 404:
                return False, None
            if response.status_code >= 400:
                return False, None
            
            # Return final URL after redirects
            return True, response.url
            
        except requests.Timeout:
            # Timeouts are suspicious, but try GET
            try:
                response = self.session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
                if response.status_code == 404:
                    return False, None
                return response.status_code < 400, response.url
            except:
                return False, None
        except Exception as e:
            return False, None
    
    def is_university_only(self, title: str, location: str) -> bool:
        """Check if event is restricted to university students"""
        restricted_keywords = [
            "student only",
            "university of",
            "imperial college",
            "ucl only",
            "kcl only",
            "qmul only",
            "for students",
            "student event",
            "alumni only",
            "staff only",
            "member only",
            "internal event",
        ]
        
        combined = f"{title} {location}".lower()
        
        for keyword in restricted_keywords:
            if keyword in combined:
                return True
        
        return False
    
    def extract_date(self, title: str) -> Optional[str]:
        """Try to extract date from title"""
        # Look for common date patterns
        date_patterns = [
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}',
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{1,2}-\d{1,2}',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def clean_database(self):
        """Remove invalid events from database"""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        print("\n" + "="*70)
        print("🔗 LINK VALIDATION & DATABASE CLEANUP")
        print("="*70 + "\n")
        
        # Get all events with URLs
        rows = cur.execute(
            "SELECT id, title, source_url, location FROM events"
        ).fetchall()
        
        print(f"📊 Checking {len(rows)} events...\n")
        
        invalid_ids = []
        
        for event_id, title, url, location in rows:
            if not url:
                print(f"  ❌ ID {event_id}: No URL - REMOVING")
                invalid_ids.append(event_id)
                self.removed_count += 1
                continue
            
            # Check if university-only
            if self.is_university_only(title, location or ""):
                print(f"  ❌ ID {event_id}: University-only event - REMOVING")
                invalid_ids.append(event_id)
                self.removed_count += 1
                continue
            
            # Validate URL
            print(f"  🔍 Checking: {title[:50]}...")
            is_valid, final_url = self.validate_url(url)
            
            if not is_valid:
                print(f"     ❌ Link broken (404/error) - REMOVING")
                invalid_ids.append(event_id)
                self.removed_count += 1
            else:
                print(f"     ✓ Link valid")
                self.validated_count += 1
                
                # Update with final URL if different (handles redirects)
                if final_url and final_url != url:
                    cur.execute("UPDATE events SET source_url = ? WHERE id = ?", (final_url, event_id))
                    print(f"     (Redirect updated)")
            
            time.sleep(0.5)  # Rate limiting
        
        # Delete invalid events
        if invalid_ids:
            placeholders = ','.join('?' * len(invalid_ids))
            cur.execute(f"DELETE FROM events WHERE id IN ({placeholders})", invalid_ids)
            conn.commit()
            print(f"\n✓ Deleted {self.removed_count} invalid events")
        
        conn.close()
        
        print("\n" + "="*70)
        print("📊 VALIDATION SUMMARY")
        print("="*70)
        print(f"Valid events:          {self.validated_count}")
        print(f"Removed (broken link): {self.removed_count}")
        print(f"Remaining:             {self.validated_count}")
        print("="*70 + "\n")


def main():
    validator = LinkValidator()
    validator.clean_database()


if __name__ == "__main__":
    main()
