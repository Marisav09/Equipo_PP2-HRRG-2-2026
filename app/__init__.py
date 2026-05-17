from __future__ import annotations

from flask import Flask

from app.core.config import settings
from app.core.logging_config import configure_logging


def create_app() -> Flask:
    configure_logging()
    settings.ensure_directories()

    flask_app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    flask_app.config["SECRET_KEY"] = "dev-secret-change-in-production"

    from app.api.routes import api

    flask_app.register_blueprint(api)
    return flask_app
