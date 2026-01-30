from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    id: Mapped[int] = mapped_column(primary_key=True)
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
    
    @classmethod
    def create(cls, **kwargs):
        """
        Crea un nuevo estudiante y lo guarda en la base de datos.
        Uso: Estudiante.create(nombre="John", apellido="Doe", cedula=123456789)
        """
        try:
            nuevo_estudiante = cls(**kwargs)
            db.session.add(nuevo_estudiante)
            db.session.commit()
            return nuevo_estudiante
        except Exception as e:
            db.session.rollback()
            raise e