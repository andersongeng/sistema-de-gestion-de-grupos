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
    from app.routes.evaluacion_route import evaluacion_bp
    from app.routes.groups_route import groups_bp

    app.register_blueprint(evaluacion_bp)
    app.register_blueprint(groups_bp)

    return app