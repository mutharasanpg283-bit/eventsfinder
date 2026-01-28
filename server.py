"""
server.py

Simple Flask server that:
- Serves "/" with a mobile-friendly list of approved, upcoming events.
- Serves "/api/events" returning JSON of the same events.

Run:
    python server.py
"""

import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, render_template, jsonify, request, session, redirect

DB_PATH = Path(__file__).parent / "database.db"

app = Flask(__name__)
app.secret_key = "events-london-admin-key-2026"  # Secret key for sessions

# Admin credentials (in production, use environment variables)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "events2026"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Ensure DB and schema exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    with open(Path(__file__).parent / "schema.sql", "r", encoding="utf-8") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()


@app.route("/")
def index():
    """Render the main page with event cards."""
    init_db()  # safe to call; CREATE IF NOT EXISTS
    conn = get_db_connection()

    # Show all events (both validated and pending)
    # This ensures newly scraped events show immediately
    rows = conn.execute(
        """
        SELECT id, title, date, location, category, is_free,
               source_name, source_url, confidence_score, is_valid
        FROM events
        ORDER BY is_valid DESC, date ASC, title ASC
        """
    ).fetchall()
    conn.close()

    events = [dict(r) for r in rows]

    return render_template("index.html", events=events)


@app.route("/api/events")
def api_events():
    """Return all events as JSON (including pending validation)."""
    init_db()
    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT id, title, date, location, category, is_free,
               source_name, source_url, confidence_score, created_at, is_valid,
               latitude, longitude
        FROM events
        ORDER BY created_at DESC, date ASC, title ASC
        """
    ).fetchall()
    conn.close()

    events = [dict(r) for r in rows]
    return jsonify(events)


@app.route("/events-map")
def events_map():
    """Render the interactive map and event discovery app."""
    init_db()
    return render_template("events_app.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Handle admin login page and authentication."""
    if request.method == "GET":
        # Check if already authenticated
        if session.get("admin_authenticated"):
            return redirect("/admin")
        return render_template("admin_login.html")
    
    # POST request: validate credentials
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["admin_authenticated"] = True
        return redirect("/admin")
    else:
        return render_template("admin_login.html", error="Invalid credentials"), 401


@app.route("/admin")
def admin_dashboard():
    """Render admin dashboard (requires authentication)."""
    # Check authentication
    if not session.get("admin_authenticated"):
        return redirect("/admin/login")
    
    init_db()
    return render_template("admin.html")


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    """Clear admin session and redirect to login."""
    session.clear()
    return redirect("/admin/login")


@app.route("/api/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """Delete an event by ID (admin only)."""
    # Check authentication
    if not session.get("admin_authenticated"):
        return jsonify({"error": "Unauthorized"}), 401
    
    init_db()
    conn = get_db_connection()
    
    try:
        # Delete the event
        conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        return jsonify({"success": True, "message": "Event deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


if __name__ == "__main__":
    # Initialize database on startup
    init_db()
    
    # Run development server
    print("🚀 Starting server at http://127.0.0.1:5000")
    print("📍 Event Map: http://127.0.0.1:5000/events-map")
    print("⚠️  Press Ctrl+C to stop")
    app.run(host="127.0.0.1", port=5000, debug=True)
