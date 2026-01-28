-- Events table
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    title TEXT,
    date TEXT,
    location TEXT,
    category TEXT,
    is_free INTEGER,
    source_name TEXT,
    source_url TEXT NOT NULL,
    confidence_score REAL,
    is_valid INTEGER DEFAULT 0,      -- 1 means AI-approved
    latitude REAL DEFAULT 51.5074,   -- London default
    longitude REAL DEFAULT -0.1278,  -- London default
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster lookup
CREATE UNIQUE INDEX IF NOT EXISTS idx_events_source_id
ON events(source_id);

CREATE INDEX IF NOT EXISTS idx_events_date
ON events(date);

CREATE INDEX IF NOT EXISTS idx_events_is_valid
ON events(is_valid);
