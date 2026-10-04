"""Error pages (HTML) and error responses (JSON for /api/)."""
from flask import jsonify, render_template, request

MESSAGES = {
    403: "You can't do that.",
    404: "That paste doesn't exist or has expired.",
    413: "That paste is too large.",
}


def _handle(err):
    msg = MESSAGES.get(err.code, "Something went wrong.")
    if request.path.startswith("/api/"):
        return jsonify(error=msg), err.code
    return render_template("error.html", code=err.code, msg=msg), err.code


def init_app(app):
    for code in MESSAGES:
        app.register_error_handler(code, _handle)
