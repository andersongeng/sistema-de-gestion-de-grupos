from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido: Mapped[str] = mapped_column(nullable=False)
    cedula: Mapped[int] = mapped_column(nullable=False, unique=True)

    grupos = relationship(
        'Grupo',
        secondary='inscripciones',
        back_populates='estudiantes'
    )

    def __repr__(self):
        return f'<Estudiante {self.cedula}: {self.nombre} {self.apellido}>'