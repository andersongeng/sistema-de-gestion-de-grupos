from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido: Mapped[str] = mapped_column(nullable=False)
    cedula: Mapped[int] = mapped_column(nullable=False, unique=True)