"""JSON API under /api."""
from flask import Blueprint, jsonify, request

from .. import pastes
from ..security import rate_limited

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.post("/paste")
def create():
    if rate_limited():
        return jsonify(error="Too many requests."), 429
    if request.mimetype == "text/plain":                 # cat file | curl ...
        data = {"content": request.get_data(as_text=True)}
    else:                                                # JSON or form
        data = request.get_json(silent=True) or request.form
    try:
        pid, token = pastes.create(data.get("content"), data.get("title"),
                                   data.get("lang", "auto"),
                                   data.get("expires", pastes.DEFAULT_EXPIRY))
    except ValueError as e:
        return jsonify(error=str(e)), 400
    base = request.host_url.rstrip("/")
    return jsonify(id=pid, url=f"{base}/{pid}", raw=f"{base}/{pid}/raw",
                   delete_token=token), 201


@bp.get("/paste/<pid>")
def read(pid):
    p = pastes.get_or_404(pid)
    return jsonify(id=p["id"], title=p["title"], lang=p["lang"],
                   content=p["content"], created=p["created"],
                   expires=p["expires"], views=p["views"])


@bp.delete("/paste/<pid>")
def remove(pid):
    p = pastes.get_or_404(pid)
    if not pastes.token_matches(p, request.headers.get("X-Delete-Token", "")):
        return jsonify(error="Invalid delete token."), 403
    pastes.delete(pid)
    return jsonify(deleted=True)
