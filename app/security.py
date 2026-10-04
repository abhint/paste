"""Rate limiting and security headers."""
import time
from collections import defaultdict, deque

from flask import current_app, request

_hits = defaultdict(deque)


def rate_limited():
    """True if this IP created too many pastes in the last minute."""
    now, queue = time.time(), _hits[request.remote_addr]
    while queue and now - queue[0] > 60:
        queue.popleft()
    if len(queue) >= current_app.config["RATE_LIMIT"]:
        return True
    queue.append(now)
    return False


def _headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'")
    return resp


def init_app(app):
    app.after_request(_headers)
