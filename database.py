"""SQLite database and OFAC list loading."""
import sqlite3
import os
from config import DATABASE_PATH, OFAC_DB_FOLDER
from ofac_parser import load_all_xml_from_folder


def get_connection():
    """Return a DB connection."""
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ofac_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                fixed_ref TEXT,
                profile_id TEXT,
                alias_type_id TEXT,
                source_file TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_ofac_name ON ofac_entries(name)"
        )
        conn.commit()
    finally:
        conn.close()


def load_ofac_data(replace=True):
    """
    Load OFAC data from all XML files in OFAC DB folder into SQLite.
    If replace=True, clears existing data first.
    """
    if not os.path.isdir(OFAC_DB_FOLDER):
        raise FileNotFoundError(f"OFAC DB folder not found: {OFAC_DB_FOLDER}")

    init_db()
    records = load_all_xml_from_folder(OFAC_DB_FOLDER)

    conn = get_connection()
    try:
        if replace:
            conn.execute("DELETE FROM ofac_entries")
        for r in records:
            conn.execute(
                """
                INSERT INTO ofac_entries (name, fixed_ref, profile_id, alias_type_id, source_file)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    r["name"],
                    r.get("fixed_ref", ""),
                    r.get("profile_id", ""),
                    r.get("alias_type_id", ""),
                    r.get("source_file", ""),
                ),
            )
        conn.commit()
        return len(records)
    finally:
        conn.close()


def get_all_names():
    """Return list of (id, name) for in-memory fuzzy matching."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT id, name, fixed_ref, profile_id, alias_type_id, source_file FROM ofac_entries"
        )
        return cur.fetchall()
    finally:
        conn.close()
