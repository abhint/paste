"""Entry point.  Dev: `python run.py`   Production: `gunicorn run:app`"""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG") == "1")
