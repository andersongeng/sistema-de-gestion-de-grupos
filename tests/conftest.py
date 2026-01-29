import pytest
from app import create_app
from app.extensions import db
from config import Config

# Definimos una clase de configuracion solo para pruebas
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False # Desactivamos CSRF para facilitar tests de formularios

@pytest.fixture
def app():
    """Crea y configura una nueva instancia de la app para cada test"""
    app = create_app(TestConfig)

    with app.app_context():
        from app.models import Estudiante, Grupo, inscripciones
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Un cliente de prueba para hacer peticiones HTTP (GET, POST, etc.)"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Un ejecutor para comandos de CLI de Flask"""
    return app.test_cli_runner()