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
    flask_app.config["SECRET_KEY"] = settings.secret_key

    from app.api.auth_routes import auth_bp
    from app.api.chat_routes import chat_bp
    from app.api.equipment_routes import equipment_bp
    from app.api.ingest_routes import ingest_bp
    from app.api.monitoring_routes import monitoring_bp
    from app.api.qr_routes import qr_bp
    from app.api.system_routes import system_bp
    from app.api.web_routes import web_bp

    flask_app.register_blueprint(web_bp)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(chat_bp, url_prefix="/api/chat")
    flask_app.register_blueprint(equipment_bp, url_prefix="/api/equipment")
    flask_app.register_blueprint(ingest_bp, url_prefix="/api/ingest")
    flask_app.register_blueprint(monitoring_bp, url_prefix="/api/monitoring")
    flask_app.register_blueprint(qr_bp, url_prefix="/api/qr")
    flask_app.register_blueprint(system_bp, url_prefix="/api/system")

    return flask_app
