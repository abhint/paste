# Paste

A small, mobile-friendly pastebin. Flask, SQLite, Pygments. No account needed.

## Project layout

    paste-app/
    ├── run.py                 Start here: `python run.py` or `gunicorn run:app`
    ├── requirements.txt       Python dependencies
    ├── app/
    │   ├── __init__.py        create_app(): connects all the parts below
    │   ├── config.py          Settings (size limit, rate limit, database path)
    │   ├── database.py        SQLite connection and the table definition
    │   ├── pastes.py          Create / read / delete logic, languages, expiry options
    │   ├── highlight.py       Syntax highlighting
    │   ├── security.py        Rate limiting and security headers
    │   ├── errors.py          Error pages and JSON errors
    │   ├── routes/
    │   │   ├── pages.py       Web pages: home, view, raw, delete
    │   │   └── api.py         JSON API (/api/paste)
    │   ├── templates/         HTML (base, index, view, error)
    │   └── static/
    │       ├── css/style.css  All styling, light and dark, mobile first
    │       ├── js/app.js      Copy buttons, theme switch, editor helpers
    │       └── img/paste.svg  Logo and favicon
    └── tests/
        └── test_app.py        Run with `python -m unittest`

Where to change things:
- A page looks wrong: `app/templates/` and `app/static/css/style.css`
- New setting or limit: `app/config.py`
- New language or expiry option: `LANGS` / `EXPIRY` in `app/pastes.py`
- New web page or API endpoint: `app/routes/pages.py` or `app/routes/api.py`

## Run

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python run.py                          # http://127.0.0.1:5000
    gunicorn -w 2 -b 0.0.0.0:8000 run:app  # production

## Settings (environment variables)
`SECRET_KEY` (set in production), `PASTE_DB` (default `paste.db`), `MAX_BYTES` (default 524288), `RATE_LIMIT` (creates per minute per IP, default 20), `DEBUG=1`.

## API
    curl -X POST http://localhost:5000/api/paste -H "Content-Type: application/json" \
         -d '{"content":"print(1)","lang":"python","expires":"1d","title":"demo"}'
    cat file.txt | curl -H "Content-Type: text/plain" --data-binary @- http://localhost:5000/api/paste
    curl http://localhost:5000/api/paste/<id>       # JSON
    curl http://localhost:5000/<id>/raw             # plain text
    curl -X DELETE http://localhost:5000/api/paste/<id> -H "X-Delete-Token: <token>"

`lang`: auto, text, python, javascript, typescript, html, css, json, yaml, bash, sql, c, cpp, java, go, rust, php, markdown.
`expires`: never, 10m, 1h, 1d, 1w, 30d.

Behind a reverse proxy, make sure the real client IP reaches the app (gunicorn `--forwarded-allow-ips` or Werkzeug `ProxyFix`), or rate limiting will see only the proxy.
