"""
ai_cleaner.py

Loads unprocessed events from the database, sends them to an AI model
to validate, clean, categorize, and assign a confidence score.

Only events with confidence >= 0.7 are marked as valid.

Run:
    python ai_cleaner.py
"""

import os
import json
import sqlite3
from datetime import datetime, date
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

DB_PATH = Path(__file__).parent / "database.db"

load_dotenv()  # load .env if present


def init_db():
    """Ensure DB and schema exist and return a connection."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    with open(Path(__file__).parent / "schema.sql", "r", encoding="utf-8") as f:
        cur.executescript(f.read())
    conn.commit()
    return conn


def fetch_unprocessed_events(conn, limit: int = 20):
    """
    Fetch events that are not yet validated by AI (is_valid = 0 and confidence_score is NULL).
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, title, date, location, is_free, source_name, source_url, created_at
        FROM events
        WHERE (confidence_score IS NULL OR is_valid = 0)
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    events = []
    for row in rows:
        events.append(
            {
                "id": row[0],
                "title": row[1],
                "date": row[2],
                "location": row[3],
                "is_free": bool(row[4]),
                "source_name": row[5],
                "source_url": row[6],
                "created_at": row[7],
            }
        )
    return events


def build_ai_prompt(events):
    """
    Build a concise prompt asking the AI to validate and categorize events.
    We ask for strict JSON output so parsing is easy.
    """
    today_str = date.today().isoformat()
    system = (
        "You are a helpful assistant that cleans and validates tech events in London.\n"
        "You must ONLY output valid JSON, no extra text.\n"
    )

    user = {
        "instructions": (
            "Given this list of event candidates, return a JSON array where each item has:\n"
            "- id (same as input id)\n"
            "- is_valid (true/false: upcoming and truly tech/computer science related in London)\n"
            "- cleaned_title (string, concise and clear)\n"
            "- category (one of: Hackathon, Workshop, Meetup, Conference, Other)\n"
            "- confidence (number 0-1)\n"
            "- date (ISO date YYYY-MM-DD; if unknown or past, treat as invalid)\n"
            "Rules:\n"
            f"- Today is {today_str}. Invalid if the event date is in the past.\n"
            "- If unsure whether it's tech-related, set is_valid=false.\n"
            "- Only keep events in LONDON or surrounding areas clearly marked as London.\n"
            "- Use confidence >= 0.7 only when you're fairly sure.\n"
            "- If you think an event is invalid, set is_valid=false and confidence<=0.6.\n"
        ),
        "events": events,
    }

    return system, json.dumps(user, ensure_ascii=False)


def call_openai(events):
    """
    Call the OpenAI API with the events and return parsed JSON results.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment (.env).")

    client = OpenAI(api_key=api_key)

    system_content, user_content = build_ai_prompt(events)

    # Using a GPT-4-level chat model. Replace with another if needed.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
        max_tokens=1500,
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse AI response as JSON: {e}\nRaw content:\n{content}")

    if not isinstance(data, list):
        raise RuntimeError("AI response is not a JSON array.")

    return data


def update_events(conn, ai_results):
    """
    Update events in DB based on AI results.
    Only keep those with confidence >= 0.7 and is_valid == true.
    """
    cur = conn.cursor()
    updated = 0
    for ev in ai_results:
        ev_id = ev.get("id")
        is_valid = bool(ev.get("is_valid"))
        confidence = float(ev.get("confidence", 0.0))
        cleaned_title = ev.get("cleaned_title") or ""
        category = ev.get("category") or "Other"
        norm_date = ev.get("date")

        if not ev_id:
            continue

        if not is_valid or confidence < 0.7:
            # Mark as invalid: set is_valid=0 and store confidence
            cur.execute(
                """
                UPDATE events
                SET is_valid = 0,
                    confidence_score = ?
                WHERE id = ?
                """,
                (confidence, ev_id),
            )
        else:
            # Approve event
            cur.execute(
                """
                UPDATE events
                SET is_valid = 1,
                    confidence_score = ?,
                    title = ?,
                    category = ?,
                    date = ?
                WHERE id = ?
                """,
                (confidence, cleaned_title, category, norm_date, ev_id),
            )
        updated += 1

    conn.commit()
    print(f"Updated {updated} events using AI results.")


def main():
    """Load unprocessed events, validate with AI, update database."""
    try:
        conn = init_db()
        try:
            events = fetch_unprocessed_events(conn, limit=20)
            if not events:
                print("No unprocessed events found.")
                return

            print(f"Sending {len(events)} events to AI for validation...")
            ai_results = call_openai(events)
            update_events(conn, ai_results)
            print("AI validation completed successfully!")
        finally:
            conn.close()
    
    except RuntimeError as e:
        print(f"ERROR: {e}")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
