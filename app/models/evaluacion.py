from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    titulo: Mapped[str] = mapped_column(nullable=False)

    