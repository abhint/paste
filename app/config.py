"""All settings live here. Override with environment variables."""
import os
import secrets


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    DB = os.environ.get("PASTE_DB", "paste.db")
    MAX_BYTES = int(os.environ.get("MAX_BYTES", 512 * 1024))   # largest paste
    RATE_LIMIT = int(os.environ.get("RATE_LIMIT", 20))         # creates/min per IP
    MAX_CONTENT_LENGTH = MAX_BYTES + 8192
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 30
