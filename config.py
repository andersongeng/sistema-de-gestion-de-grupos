import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError("No se ha configurado una SECRET_KEY. La aplicación no puede iniciar.")
    
    # Flask configuration
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_ENV = os.environ.get('FLASK_ENV')

    # DB Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')