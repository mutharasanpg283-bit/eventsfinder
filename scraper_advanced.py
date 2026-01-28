"""
scraper_advanced.py

Advanced multi-source event scraper for London tech events.
Handles 46+ different websites with intelligent parsing, rate limiting, and error handling.

Run:
    python scraper_advanced.py

Features:
    - Multiple source support (EventBrite, Meetup, Hackathons, Universities, etc.)
    - Smart HTML parsing with fallback selectors
    - Rate limiting to respect websites
    - Proper user agents
    - Error handling and recovery
    - Progress tracking
"""

import sqlite3
import requests
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import re

DB_PATH = Path(__file__).parent / "database.db"

# User agent list for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]

EVENT_SOURCES = [
    # General Event Platforms - Fast/Reliable
    ("https://www.eventbrite.co.uk/d/united-kingdom--london/technology--events", "eventbrite"),
    ("https://londontechweek.com", "ltw"),
    ("https://www.feverup.com/london", "fever"),
    
    # Hackathons & Developer Events - Faster subset
    ("https://devpost.com/hackathons?search=london", "devpost"),
    ("https://mlh.io/seasons/2026/events", "mlh"),
    ("https://www.hackerearth.com/challenges", "hackerearth"),
    ("https://angelhack.com", "angelhack"),
    ("https://itch.io/jams", "itch"),
    ("https://www.kaggle.com/competitions", "kaggle"),
    
    # University Events (London) - Select few
    ("https://www.imperial.ac.uk/events", "imperial"),
    ("https://www.ucl.ac.uk/events", "ucl"),
    
    # Workshops & Communities - Reliable ones
    ("https://generalassemb.ly/events", "ga"),
    ("https://www.lewagon.com/events", "lewagon"),
    ("https://codebar.io/events", "codebar"),
    ("https://www.womenwhocode.com/london", "wwc"),
    ("https://technation.io/events", "technation"),
    ("https://www.startupgrind.com/london", "startupgrind"),
]


class EventScraper:
    """Handles scraping from multiple sources with intelligent parsing."""
    
    def __init__(self):
        self.session = requests.Session()
        self.events_found = 0
        self.events_inserted = 0
        self.errors = 0
        
    def get_random_user_agent(self) -> str:
        """Return a random user agent."""
        return random.choice(USER_AGENTS)
    
    def safe_fetch(self, url: str, timeout: int = 8, delay: float = 0.5) -> Optional[str]:
        """
        Safely fetch URL with user agent rotation, error handling, and rate limiting.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            delay: Delay between requests in seconds
            
        Returns:
            HTML content or None if failed
        """
        try:
            time.sleep(delay)  # Rate limiting
            headers = {"User-Agent": self.get_random_user_agent()}
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"  ❌ Failed to fetch {url}: {str(e)[:80]}")
            self.errors += 1
            return None
    
    def init_db(self):
        """Ensure the database and schema exist."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        with open(Path(__file__).parent / "schema.sql", "r", encoding="utf-8") as f:
            cur.executescript(f.read())
        conn.commit()
        return conn
    
    def event_exists(self, conn, source_id: str) -> bool:
        """Check if an event with this source_id already exists."""
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM events WHERE source_id = ?", (source_id,))
            return cur.fetchone() is not None
        except:
            return False
    
    def insert_event(self, conn, event: Dict) -> bool:
        """Insert a single event into the database."""
        try:
            if self.event_exists(conn, event["source_id"]):
                return False
            
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO events (
                    source_id, title, date, location, category,
                    is_free, source_name, source_url,
                    confidence_score, is_valid
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event["source_id"],
                    event["title"],
                    event.get("date"),
                    event.get("location", "London"),
                    event.get("category"),
                    event.get("is_free", 0),
                    event["source"],
                    event["url"],
                    None,
                    0,
                ),
            )
            conn.commit()
            self.events_inserted += 1
            return True
        except Exception as e:
            print(f"  ⚠️  Failed to insert event: {str(e)[:60]}")
            return False
    
    # ===== PARSER FUNCTIONS FOR DIFFERENT SOURCES =====
    
    def parse_eventbrite(self, html: str, source_url: str) -> List[Dict]:
        """Parse EventBrite London tech events."""
        events = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # EventBrite event cards
            cards = soup.find_all("article", attrs={"data-event-id": True})
            if not cards:
                cards = soup.find_all("div", class_=re.compile("EventCard"))
            
            for card in cards[:15]:  # Limit to 15 per source
                try:
                    # Title
                    title_el = card.find(["h2", "h3"])
                    if not title_el:
                        title_el = card.find("a", {"class": re.compile("event-title")})
                    title = title_el.get_text(strip=True) if title_el else None
                    
                    if not title:
                        continue
                    
                    # URL
                    link = card.find("a", href=True)
                    url = link["href"] if link else None
                    if not url or "eventbrite" not in url:
                        url = source_url
                    
                    # Date
                    date_el = card.find(["time", "span"], {"data-spec": re.compile("date")})
                    date_text = date_el.get_text(strip=True) if date_el else None
                    
                    # Location
                    loc_el = card.find(["span", "div"], {"data-spec": re.compile("location|sub-title")})
                    location = loc_el.get_text(strip=True) if loc_el else "London"
                    
                    # Free?
                    is_free = 0
                    price_el = card.find(["span", "div"], class_=re.compile("price|free"))
                    if price_el and "free" in price_el.get_text().lower():
                        is_free = 1
                    
                    source_id = f"eventbrite_{title}_{date_text}".replace(" ", "_")[:50]
                    
                    events.append({
                        "source_id": source_id,
                        "title": title[:150],
                        "date": date_text,
                        "location": location[:100],
                        "is_free": is_free,
                        "source": "EventBrite",
                        "url": url,
                        "category": "tech",
                    })
                except Exception as e:
                    continue
        except Exception as e:
            print(f"    Error parsing EventBrite: {str(e)[:60]}")
        
        return events
    
    def parse_meetup(self, html: str, source_url: str) -> List[Dict]:
        """Parse Meetup events."""
        events = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # Meetup event listings
            event_els = soup.find_all("a", {"class": re.compile("eventCardHead")})
            if not event_els:
                event_els = soup.find_all("div", {"class": re.compile("eventCard")})
            
            for el in event_els[:15]:
                try:
                    title = el.get_text(strip=True) if el else None
                    if not title or len(title) < 3:
                        continue
                    
                    # Try to find URL
                    link = el.find("a", href=True) or el
                    url = link.get("href", source_url) if hasattr(link, "get") else source_url
                    
                    source_id = f"meetup_{title}".replace(" ", "_")[:50]
                    
                    events.append({
                        "source_id": source_id,
                        "title": title[:150],
                        "date": None,
                        "location": "London",
                        "is_free": 1,  # Meetup is usually free
                        "source": "Meetup",
                        "url": url,
                        "category": "tech",
                    })
                except Exception as e:
                    continue
        except Exception as e:
            print(f"    Error parsing Meetup: {str(e)[:60]}")
        
        return events
    
    def parse_devpost(self, html: str, source_url: str) -> List[Dict]:
        """Parse DevPost hackathons."""
        events = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # DevPost hackathon entries
            hackathons = soup.find_all("a", {"class": re.compile("hackathon-card")})
            if not hackathons:
                hackathons = soup.find_all("div", {"class": re.compile("hackathon")})
            
            for hack in hackathons[:15]:
                try:
                    title_el = hack.find("h2") or hack.find("a")
                    title = title_el.get_text(strip=True) if title_el else None
                    
                    if not title or len(title) < 3:
                        continue
                    
                    url = hack.get("href", source_url) if hasattr(hack, "get") else source_url
                    
                    source_id = f"devpost_{title}".replace(" ", "_")[:50]
                    
                    events.append({
                        "source_id": source_id,
                        "title": title[:150],
                        "date": None,
                        "location": "London",
                        "is_free": 1,
                        "source": "DevPost",
                        "url": url,
                        "category": "hackathon",
                    })
                except Exception as e:
                    continue
        except Exception as e:
            print(f"    Error parsing DevPost: {str(e)[:60]}")
        
        return events
    
    def parse_generic_html(self, html: str, source_url: str, source_name: str) -> List[Dict]:
        """Generic HTML parser for sites with event listings."""
        events = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # Common event selectors
            selectors = [
                ("article", {}),
                ("div", {"class": re.compile("event|Event")}),
                ("li", {"class": re.compile("event|Event")}),
            ]
            
            found_elements = []
            for tag, attrs in selectors:
                found_elements.extend(soup.find_all(tag, attrs, limit=20))
            
            if not found_elements:
                # Fallback: look for any links with event keywords
                all_links = soup.find_all("a", href=True)
                for link in all_links[:10]:
                    text = link.get_text(strip=True)
                    if any(keyword in text.lower() for keyword in ["event", "workshop", "meetup", "talk", "conference", "summit"]):
                        events.append({
                            "source_id": f"{source_name}_{text}".replace(" ", "_")[:50],
                            "title": text[:150],
                            "date": None,
                            "location": "London",
                            "is_free": 0,
                            "source": source_name,
                            "url": link.get("href", source_url),
                            "category": "tech",
                        })
                return events
            
            for element in found_elements[:15]:
                try:
                    # Try to extract title
                    title_el = element.find(["h2", "h3", "a"])
                    title = title_el.get_text(strip=True) if title_el else None
                    
                    if not title or len(title) < 3:
                        continue
                    
                    # Try to extract URL
                    link = element.find("a", href=True)
                    url = link["href"] if link else source_url
                    
                    # Try to extract date (common patterns)
                    date_el = element.find(["time", "span"], class_=re.compile("date|time"))
                    date_text = date_el.get_text(strip=True) if date_el else None
                    
                    source_id = f"{source_name}_{title}".replace(" ", "_")[:50]
                    
                    events.append({
                        "source_id": source_id,
                        "title": title[:150],
                        "date": date_text,
                        "location": "London",
                        "is_free": 0,
                        "source": source_name,
                        "url": url,
                        "category": "tech",
                    })
                except Exception as e:
                    continue
        except Exception as e:
            print(f"    Error in generic parser: {str(e)[:60]}")
        
        return events
    
    def scrape_source(self, url: str, source_type: str) -> List[Dict]:
        """Scrape a single source and extract events."""
        print(f"📍 Scraping {source_type}...")
        
        html = self.safe_fetch(url)
        if not html:
            return []
        
        # Route to appropriate parser
        parsers = {
            "eventbrite": self.parse_eventbrite,
            "meetup": self.parse_meetup,
            "devpost": self.parse_devpost,
        }
        
        parser = parsers.get(source_type, self.parse_generic_html)
        
        if source_type in parsers:
            events = parser(html, url)
        else:
            events = self.parse_generic_html(html, url, source_type.title())
        
        self.events_found += len(events)
        print(f"  ✓ Found {len(events)} events")
        return events
    
    def scrape_all_sources(self) -> int:
        """Scrape all configured sources."""
        conn = self.init_db()
        
        print("\n" + "="*60)
        print("🚀 LONDON TECH EVENTS SCRAPER - MULTI-SOURCE")
        print("="*60 + "\n")
        
        for url, source_type in EVENT_SOURCES:
            try:
                events = self.scrape_source(url, source_type)
                
                for event in events:
                    self.insert_event(conn, event)
                
            except Exception as e:
                print(f"  ❌ Error with {source_type}: {str(e)[:60]}")
                self.errors += 1
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ SCRAPING COMPLETE")
        print("="*60)
        print(f"Total events found:   {self.events_found}")
        print(f"Events inserted:      {self.events_inserted}")
        print(f"Errors encountered:   {self.errors}")
        print("="*60 + "\n")
        
        return self.events_inserted


def scrape_london_tech_events():
    """Main entry point."""
    try:
        scraper = EventScraper()
        scraper.scrape_all_sources()
        print("✨ Events now available in database!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    scrape_london_tech_events()
