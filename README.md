# Paste

**Paste** is a small web app for sharing text. You paste text (a note, a log, some code), press one button, and get a short link. Anyone you send the link to can read it. No account, no sign-up.

It works on phones and computers, has light and dark themes, and also has a simple API so scripts can create pastes.

## What it is good for

- Sending someone a code snippet, error log, or config file without attaching a file.
- Moving text from your phone to your computer (or the other way) through a link.
- Sharing temporary text that should disappear on its own (it can expire after 10 minutes to 30 days).
- Letting scripts and terminals publish output: `cat log.txt | curl ...` returns a link.

## What it is not

- **Not private.** Anyone who has the link can read the paste. Do not put passwords, keys, or personal data in it.
- **Not encrypted.** The text is stored as plain text in a database file on the server.
- **Not permanent storage.** Pastes can expire, and you should keep your own copy of anything important.

---

## 1. Get it running

You need Python 3.10 or newer.

**Windows (PowerShell or Command Prompt)**

    cd paste
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python run.py

**Linux or macOS**

    cd paste
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python run.py

Then open **http://127.0.0.1:5000** in your browser. Stop the app with `Ctrl+C`.

To open it on your phone while testing, connect the phone to the same Wi-Fi, run `python run.py` after changing the last line of `run.py` to `app.run(host="0.0.0.0")`, and visit `http://<your-computer-ip>:5000` on the phone.

---

## 2. How to use it (website)

### Create a paste
1. Open the home page.
2. Type or paste your text into the big box. You can also **drag a text file** onto the box.
3. Optional settings above the box:
   - **Title**: a name for the paste (up to 100 characters).
   - **Language**: pick one for syntax colours, or leave on *Auto-detect*.
   - **Expires**: how long the paste lives. Default is 1 week. *Never* keeps it until deleted.
4. Press **Create paste** (or `Ctrl+Enter` / `⌘+Enter`).

A counter under the box shows the size. The limit is 512 KB by default.

### Share it
You land on the paste page. Press **Copy link** and send the link to anyone.

### On the paste page
| Button | What it does |
|---|---|
| Copy link | Copies the page address |
| Copy text | Copies the full text, ready to paste elsewhere |
| Raw | Opens the plain text only (good for `curl` or `wget`) |
| Download | Saves the text as `paste-<id>.txt` |
| New paste | Back to the home page |
| Delete | Removes the paste for good. **Only you see this button**, see below |

The line under the title shows the language, number of lines, views, creation time, and expiry time.

### Deleting
The browser you created the paste in is remembered (a cookie, kept for 30 days, for your last 10 pastes), so the **Delete** button appears for you only. If you clear cookies or use another device, you can't delete from the website. Use the API delete token (section 3) or let the paste expire.

### Light and dark
The **◐** button in the top right switches theme. Your choice is saved in your browser. By default the app follows your device setting.

### Keyboard shortcuts
- `Ctrl+Enter` or `⌘+Enter` in the editor: create the paste.

---

## 3. How to use it (API and command line)

Base address in these examples is `http://127.0.0.1:5000`. Replace it with your server's address.

### Create a paste
Fields: `content` (required), `title`, `lang`, `expires`.

**Send plain text from a file or command (Linux, macOS, Git Bash):**

    cat notes.txt | curl -H "Content-Type: text/plain" --data-binary @- http://127.0.0.1:5000/api/paste

**Send JSON:**

    curl -X POST http://127.0.0.1:5000/api/paste \
         -H "Content-Type: application/json" \
         -d '{"content":"print(1)","lang":"python","expires":"1d","title":"demo"}'

**Windows PowerShell:**

    Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/paste `
      -ContentType "application/json" `
      -Body '{"content":"print(1)","lang":"python","expires":"1d"}'

**Python:**

    import requests
    r = requests.post("http://127.0.0.1:5000/api/paste",
                      json={"content": "print(1)", "lang": "python"})
    print(r.json()["url"])

The response (status 201):

    {
      "id": "zhNvpKPx",
      "url": "http://127.0.0.1:5000/zhNvpKPx",
      "raw": "http://127.0.0.1:5000/zhNvpKPx/raw",
      "delete_token": "…keep this to delete the paste later…"
    }

**Save the `delete_token`.** It is shown only once.

### Read a paste

    curl http://127.0.0.1:5000/api/paste/<id>     # JSON with title, lang, content, times, views
    curl http://127.0.0.1:5000/<id>/raw           # just the text

### Delete a paste

    curl -X DELETE http://127.0.0.1:5000/api/paste/<id> -H "X-Delete-Token: <delete_token>"

### Allowed values
- `lang`: `auto`, `text`, `python`, `javascript`, `typescript`, `html`, `css`, `json`, `yaml`, `bash`, `sql`, `c`, `cpp`, `java`, `go`, `rust`, `php`, `markdown`. Unknown values fall back to `auto`.
- `expires`: `never`, `10m`, `1h`, `1d`, `1w`, `30d`. Default `1w`. Unknown values fall back to `1w`.

### Error responses
Errors come back as JSON like `{"error": "The paste is empty."}`.

| Status | Meaning |
|---|---|
| 400 | Empty paste or too large |
| 403 | Wrong delete token |
| 404 | Paste doesn't exist or has expired |
| 413 | Request body too large |
| 429 | Too many pastes from your address, wait a minute |

---

## 4. Settings

Settings are read from environment variables. All are optional.

| Variable | Default | Meaning |
|---|---|---|
| `SECRET_KEY` | random each start | Signs the cookie that remembers your delete rights. **Set it in production**, or the Delete button stops working after every restart. |
| `PASTE_DB` | `paste.db` | Path of the SQLite database file |
| `MAX_BYTES` | `524288` (512 KB) | Largest allowed paste |
| `RATE_LIMIT` | `20` | Pastes allowed per minute per IP address |
| `DEBUG` | off | Set to `1` for auto-reload and detailed errors (development only) |

Setting a variable:

    # Windows PowerShell
    $env:SECRET_KEY = "a-long-random-string"
    python run.py

    # Linux / macOS
    export SECRET_KEY="a-long-random-string"
    python run.py

Make a good key with: `python -c "import secrets; print(secrets.token_hex(32))"`

---

## 5. Running it for real (production)

`python run.py` is for testing. For a real server use a production server:

    # Windows
    waitress-serve --listen=0.0.0.0:8000 run:app

    # Linux / macOS
    gunicorn -w 2 -b 0.0.0.0:8000 run:app

(`gunicorn` does not run on Windows because it needs the Unix-only `fcntl` module, so Windows uses `waitress`.)

Checklist:
- Set `SECRET_KEY`.
- Put it behind HTTPS (for example nginx or Caddy as a reverse proxy).
- Behind a proxy, make sure the real visitor address reaches the app (gunicorn `--forwarded-allow-ips`, or wrap the app in Werkzeug's `ProxyFix`), otherwise the rate limit sees only the proxy.
- Back up by copying the `paste.db` file.
- The rate limit is kept in memory per worker, so it resets on restart and each worker counts separately.

---

## 6. How it works (short)

1. You submit text. `app/routes/pages.py` (or `api.py`) receives it.
2. `app/pastes.py` checks it (not empty, not too big), makes a random 8-character id and a random delete token, and saves it in SQLite (`app/database.py`).
3. When someone opens `/<id>`, the paste is loaded, its view count goes up, and `app/highlight.py` colours it with Pygments.
4. Expired pastes are deleted when someone opens them and whenever a new paste is created.
5. Your browser keeps the delete token in a signed cookie, which is how the Delete button knows it's you.

Security basics included: size limit, per-IP rate limit, plain-text raw view with `nosniff`, a strict content security policy, and escaped output.

---

## 7. Project layout

    paste/
    ├── run.py                 Start here: python run.py
    ├── requirements.txt       Python packages
    ├── README.md              This file
    ├── app/
    │   ├── __init__.py        create_app(): connects all the parts
    │   ├── config.py          Settings
    │   ├── database.py        SQLite connection and table
    │   ├── pastes.py          Create / read / delete logic, languages, expiry options
    │   ├── highlight.py       Syntax highlighting
    │   ├── security.py        Rate limiting and security headers
    │   ├── errors.py          Error pages and JSON errors
    │   ├── routes/
    │   │   ├── pages.py       Web pages: home, view, raw, delete
    │   │   └── api.py         JSON API (/api/paste)
    │   ├── templates/         HTML: base, index, view, error
    │   └── static/            css/style.css, js/app.js, img/paste.svg
    └── tests/
        └── test_app.py        Automatic tests

Where to change things:
- A page looks wrong: `app/templates/` and `app/static/css/style.css`
- A new limit or setting: `app/config.py`
- A new language or expiry option: `LANGS` / `EXPIRY` in `app/pastes.py`
- A new page or API endpoint: `app/routes/pages.py` or `app/routes/api.py`

Run the tests with `python -m unittest` from the top folder.

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'fcntl'` | You ran `gunicorn` on Windows. Use `python run.py` or `waitress-serve` instead. |
| `BuildError: Could not build url for endpoint 'index'` (or `'pygments_css'`, `'raw'`, `'delete'`) | A template is an old copy. Page routes live in a group called `pages`, so every `url_for` must say `pages.index`, `pages.raw`, `pages.delete`, `pages.pygments_css`. Use the current files in `app/templates/`. |
| `ModuleNotFoundError: No module named 'flask'` (or `pygments`) | Activate the virtual environment, then run `pip install -r requirements.txt`. |
| `No module named 'app'` | Run commands from the top folder, where `run.py` is, not from inside `app/`. |
| Delete button missing | You're on another browser or device, or cookies were cleared, or `SECRET_KEY` changed. Use the API delete token or wait for expiry. |
| "Too many pastes" | The rate limit hit. Wait a minute or raise `RATE_LIMIT`. |
| "The paste is too large" | Over 512 KB. Shorten it or raise `MAX_BYTES`. |
| Page looks unstyled | Check `app/static/css/style.css` exists and the app was restarted. |
| `python -m unittest` says 0 tests | Make sure `tests/__init__.py` exists (it can be empty). |

---

## 9. Limits and ideas for later

Current limits: no accounts, no passwords on pastes, no editing after creating, no search or list of pastes (links are the only way in), no burn-after-reading.

License: add the license of your choice (the original repository uses MIT).