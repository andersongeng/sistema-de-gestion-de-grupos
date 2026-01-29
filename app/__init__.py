from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app(config_class=Config):
    # Create app instance and fill configuration
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    from app import models

    migrate.init_app(app, db)

    # Register blueprints

    return app