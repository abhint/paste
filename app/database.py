"""SQLite connection and table definition."""
import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS pastes (
    id      TEXT PRIMARY KEY,
    title   TEXT,
    content TEXT NOT NULL,
    lang    TEXT NOT NULL,
    created INTEGER NOT NULL,
    expires INTEGER,
    token   TEXT NOT NULL,
    views   INTEGER NOT NULL DEFAULT 0
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB"])
        g.db.row_factory = sqlite3.Row
    return g.db


def _close(_exc=None):
    conn = g.pop("db", None)
    if conn:
        conn.close()


def init_app(app):
    app.teardown_appcontext(_close)
    conn = sqlite3.connect(app.config["DB"])
    conn.executescript(SCHEMA)
    conn.close()
