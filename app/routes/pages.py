"""Web pages: create form, view, raw text, delete, highlight CSS."""
from flask import (Blueprint, Response, abort, current_app, redirect,
                   render_template, request, session, url_for)

from .. import highlight, pastes
from ..security import rate_limited

bp = Blueprint("pages", __name__)


def _remember(pid, token):
    """Keep the delete token in the creator's cookie (last 10 pastes)."""
    tokens = session.get("tokens", {})
    tokens[pid] = token
    session["tokens"] = dict(list(tokens.items())[-10:])
    session.permanent = True


@bp.route("/", methods=["GET", "POST"])
def index():
    err = None
    if request.method == "POST":
        if rate_limited():
            err = "Too many pastes. Wait a minute and try again."
        else:
            f = request.form
            try:
                pid, token = pastes.create(f.get("content"), f.get("title"),
                                           f.get("lang"), f.get("expires"))
            except ValueError as e:
                err = str(e)
            else:
                _remember(pid, token)
                return redirect(url_for("pages.view", pid=pid))
    page = render_template(
        "index.html", langs=pastes.LANGS, expiry=pastes.EXPIRY,
        default_expiry=pastes.DEFAULT_EXPIRY, err=err, form=request.form,
        max_kb=current_app.config["MAX_BYTES"] // 1024)
    return page, (400 if err else 200)


@bp.get("/<pid>")
def view(pid):
    paste = pastes.get_or_404(pid)
    pastes.add_view(pid)
    html, lang_name = highlight.render(paste)
    return render_template(
        "view.html", p=paste, html=html, lang_name=lang_name,
        created=pastes.fmt_time(paste["created"]),
        expires=pastes.fmt_time(paste["expires"]),
        owner=pastes.token_matches(paste, session.get("tokens", {}).get(pid)),
        lines=paste["content"].count("\n") + 1)


@bp.get("/<pid>/raw")
def raw(pid):
    paste = pastes.get_or_404(pid)
    resp = Response(paste["content"], mimetype="text/plain")
    if request.args.get("download"):
        resp.headers["Content-Disposition"] = f'attachment; filename="paste-{pid}.txt"'
    return resp


@bp.post("/<pid>/delete")
def delete(pid):
    paste = pastes.get_or_404(pid)
    token = request.form.get("token") or session.get("tokens", {}).get(pid)
    if not pastes.token_matches(paste, token):
        abort(403)
    pastes.delete(pid)
    return redirect(url_for("pages.index"))


@bp.get("/pygments.css")
def pygments_css():
    return Response(highlight.theme_css(), mimetype="text/css",
                    headers={"Cache-Control": "public, max-age=86400"})
