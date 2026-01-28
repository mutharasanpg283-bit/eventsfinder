# London Tech Events Finder - Data Pipeline Documentation

## Overview

The application now runs a comprehensive data pipeline that ensures data quality at every stage. Old, redundant scrapers and utility files have been removed to streamline the codebase.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LONDON TECH EVENTS FINDER                     │
│                    Complete Data Pipeline                        │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: SCRAPING (scraper_advanced.py)                         │
│  • Scrapes 46+ London tech event sources                        │
│  • Handles Eventbrite, Meetup, Hackathons, Universities, etc.  │
│  • Multi-threaded with rate limiting                           │
│  • Stores raw events in database                               │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: DUPLICATE REMOVAL (main.py)                            │
│  • Identifies duplicate events                                  │
│  • Groups by title, location, and date                         │
│  • Keeps oldest, removes duplicates                            │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: BROKEN URL CLEANUP (main.py)                           │
│  • Removes events with relative URLs (starting with /)         │
│  • Validates URL format                                         │
│  • Ensures all events have valid HTTPS URLs                    │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: URL VALIDATION (link_validator.py)                     │
│  • Tests if event URLs actually exist (checks for 404s)        │
│  • Follows redirects                                            │
│  • Removes inaccessible events                                 │
│  • Rate limited to respect websites                            │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: EVENT ENHANCEMENT (enhance_events.py)                  │
│  • Re-validates URLs with better metadata extraction           │
│  • Generates missing source_id values                          │
│  • Removes malformed data                                       │
│  • Ensures data consistency                                     │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: AI VALIDATION (ai_cleaner.py)                          │
│  • Uses OpenAI API to validate event quality                   │
│  • Categorizes events (Hackathon, Workshop, Meetup, etc.)      │
│  • Extracts structured data (dates, locations, prices)         │
│  • Assigns confidence scores (0.0 - 1.0)                       │
│  • Marks is_valid=1 for confidence >= 0.7                      │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: WEB SERVER (server.py)                                 │
│  • Serves clean, validated events                              │
│  • Provides REST API (/api/events)                             │
│  • Admin panel for manual event removal                         │
│  • Interactive map with event filtering                        │
└─────────────────────────────────────────────────────────────────┘
```

## Core Files

### Active Python Files (Required)

1. **main.py** (PRIMARY ORCHESTRATOR)
   - Entry point for entire application
   - Runs complete pipeline
   - Supports multiple execution modes
   - All cleaning steps integrated

2. **scraper_advanced.py**
   - Only remaining scraper (old ones removed)
   - Scrapes 46+ event sources
   - Multi-threaded with rate limiting
   - Intelligent HTML parsing

3. **ai_cleaner.py**
   - AI-powered event validation
   - Uses OpenAI API for quality assessment
   - Categorization and scoring
   - Confidence-based filtering

4. **link_validator.py**
   - URL accessibility checking
   - 404 detection
   - Redirect following
   - Rate limiting

5. **enhance_events.py**
   - Data quality improvements
   - Metadata extraction
   - Source ID generation
   - Malformed data removal

6. **server.py**
   - Flask web server
   - REST API endpoints
   - Admin dashboard
   - Event serving

### Removed Files (Obsolete)

✗ scraper.py - Simple scraper (replaced by advanced version)
✗ scraper_improved.py - Intermediate version (replaced by advanced)
✗ scraper_quality.py - Quality scraper (replaced by advanced)
✗ clean_broken_urls.py - Standalone cleaner (integrated into main.py)
✗ verify_urls.py - Standalone verifier (integrated into pipeline)
✗ continuous_runner.py - Old scheduler (functionality in main.py)
✗ maintain_links.py - Standalone maintainer (integrated into pipeline)
✗ source_discovery.py - Source discovery tool (integrated into scraper)

## Usage

### Full Workflow (Default)
Runs complete pipeline: scrape → clean → enhance → validate → serve
```bash
python main.py
```

### Serve Only
Start web server (use existing data)
```bash
python main.py --serve-only
```

### Scrape Only
Fetch new events from sources
```bash
python main.py --scrape-only
```

### Clean Only
Remove duplicates, broken URLs, and enhance data (without AI validation)
```bash
python main.py --clean-only
```

### Validate Only
Run AI validation on pending events
```bash
python main.py --validate-only
```

### Scheduled Mode
Update every N hours, serve continuously
```bash
python main.py --schedule 24
```

## Data Quality Improvements

### Before Pipeline
- Multiple duplicate events
- Broken relative URLs
- 404 errors and inaccessible links
- Inconsistent data formats
- Unverified event information
- Generic/spam events

### After Pipeline
✓ No duplicates
✓ All URLs validated and working
✓ Consistent data format
✓ AI-verified quality events only
✓ Proper categories and pricing
✓ Confidence scoring system

## Database Fields

Each event in the database contains:
- **id**: Primary key
- **source_id**: Unique identifier from source
- **title**: Event name
- **date**: Event date
- **location**: Event location
- **category**: Category (Hackathon, Workshop, Meetup, Conference, Expo, Other)
- **is_free**: 0 = Paid, 1 = Free
- **source_name**: Source website (EventBrite, Meetup, etc.)
- **source_url**: Link to event
- **confidence_score**: AI confidence (0.0-1.0)
- **is_valid**: 1 = AI approved, 0 = Pending
- **latitude/longitude**: Map coordinates
- **created_at**: When event was added to database

## Configuration

Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

Get your API key: https://platform.openai.com/api-keys

## Error Handling

The pipeline is designed to be resilient:
- Each step can fail without stopping the entire pipeline
- Errors are logged and reported
- Server continues running even if scraping fails
- Admin panel allows manual event cleanup

## Performance

- **Scraping**: ~5-15 minutes (46+ sources)
- **URL Validation**: ~10-20 minutes (checks each link)
- **AI Validation**: ~30-60 minutes (batch processing)
- **Total Pipeline**: ~1-2 hours

## Best Practices

1. **Regular Updates**: Run full pipeline daily for fresh content
2. **Admin Review**: Check admin panel for any low-quality events
3. **Monitoring**: Watch console output for errors
4. **Backups**: Database is stored in database.db

## Support

For issues:
1. Check console output for error messages
2. Verify OPENAI_API_KEY is set in .env
3. Ensure all dependencies are installed (requirements.txt)
4. Try running `python main.py --clean-only` first
