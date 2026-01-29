import os
from config import Config

def test_config_secret_key():
    """Verifica que la app use la clave del .env"""
    # Escenario A: No hay variable de entorno
    if 'SECRET_KEY' in os.environ:
        del os.environ['SECRET_KEY']

    config = Config()
    assert config.SECRET_KEY is not None

def test_config_database_url():
    """Verifica que la base de datos sea SQLite por defecto"""

    config = Config()
    assert 'sqlite' in config.SQLALCHEMY_DATABASE_URI