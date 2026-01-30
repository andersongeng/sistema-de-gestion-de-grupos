from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        """
        Method to create any record.
        """
        nuevo_objeto = cls(**kwargs)
        db.session.add(nuevo_objeto)
        db.session.commit()
        return nuevo_objeto

db = SQLAlchemy(model_class=Base)
migrate = Migrate()