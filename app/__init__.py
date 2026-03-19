from flask import Flask

from config import Config
from .extensions import db, migrate
from .routes.main import main_bp


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    app.register_blueprint(main_bp)

    @app.cli.command("init-db")
    def init_db() -> None:
        db.create_all()
        print("Database initialized.")

    @app.cli.command("reset-db")
    def reset_db() -> None:
        db.drop_all()
        db.create_all()
        print("Database reset (all tables dropped and recreated).")

    return app
