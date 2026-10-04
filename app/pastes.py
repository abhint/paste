"""Paste logic: create, read, delete. No web code in here."""
import secrets
import time
from datetime import datetime, timezone

from flask import abort, current_app

from .database import get_db

LANGS = {
    "Auto-detect": "auto", "Plain text": "text", "Python": "python",
    "JavaScript": "javascript", "TypeScript": "typescript", "HTML": "html",
    "CSS": "css", "JSON": "json", "YAML": "yaml", "Bash": "bash",
    "SQL": "sql", "C": "c", "C++": "cpp", "Java": "java", "Go": "go",
    "Rust": "rust", "PHP": "php", "Markdown": "markdown",
}
EXPIRY = {  # key: (label, seconds or None)
    "never": ("Never", None), "10m": ("10 minutes", 600),
    "1h": ("1 hour", 3600), "1d": ("1 day", 86400),
    "1w": ("1 week", 604800), "30d": ("30 days", 2592000),
}
DEFAULT_EXPIRY = "1w"


def create(content, title, lang, expires):
    """Save a paste. Returns (id, delete_token). Raises ValueError on bad input."""
    max_bytes = current_app.config["MAX_BYTES"]
    content = (content or "").replace("\r\n", "\n")
    if not content.strip():
        raise ValueError("The paste is empty.")
    if len(content.encode()) > max_bytes:
        raise ValueError(f"The paste is too large (max {max_bytes // 1024} KB).")

    lang = lang if lang in LANGS.values() else "auto"
    expires = expires if expires in EXPIRY else DEFAULT_EXPIRY
    now = int(time.time())
    secs = EXPIRY[expires][1]
    pid, token = secrets.token_urlsafe(6), secrets.token_urlsafe(16)

    db = get_db()
    db.execute("DELETE FROM pastes WHERE expires IS NOT NULL AND expires < ?", (now,))
    db.execute(
        "INSERT INTO pastes (id,title,content,lang,created,expires,token) VALUES (?,?,?,?,?,?,?)",
        (pid, (title or "").strip()[:100] or None, content, lang, now,
         now + secs if secs else None, token))
    db.commit()
    return pid, token


def get_or_404(pid):
    db = get_db()
    row = db.execute("SELECT * FROM pastes WHERE id = ?", (pid,)).fetchone()
    if row and row["expires"] and row["expires"] < time.time():
        delete(pid)
        row = None
    if not row:
        abort(404)
    return row


def add_view(pid):
    db = get_db()
    db.execute("UPDATE pastes SET views = views + 1 WHERE id = ?", (pid,))
    db.commit()


def delete(pid):
    db = get_db()
    db.execute("DELETE FROM pastes WHERE id = ?", (pid,))
    db.commit()


def token_matches(paste, token):
    return bool(token) and secrets.compare_digest(token, paste["token"])


def fmt_time(ts):
    if not ts:
        return "Never"
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
