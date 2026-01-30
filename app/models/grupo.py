from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Grupo(db.Model):
    __tablename__ = 'grupos'

    numero: Mapped[int] = mapped_column(nullable=False)
    evaluacion_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('evaluaciones.id'), nullable=False)
    
    estudiantes = relationship(
        'Estudiante',
        secondary='inscripciones',
        back_populates='grupos'
    )

    def __repr__(self):
        return f'<Grupo numero: {self.numero}>'