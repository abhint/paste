"""Application factory: builds the app and plugs the parts together."""
from flask import Flask

from . import database, errors, security
from .config import Config
from .routes import api, pages


def create_app(overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.update(overrides or {})      # tests pass their own settings

    database.init_app(app)
    security.init_app(app)
    errors.init_app(app)
    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp)
    return app
