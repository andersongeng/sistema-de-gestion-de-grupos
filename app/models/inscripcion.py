import sqlalchemy as sa
from app.extensions import db

inscripciones = db.Table(
    'inscripciones',
    sa.Column('estudiante_id', sa.Integer, sa.ForeignKey('estudiantes.id'), primary_key=True),
    sa.Column('grupo_id', sa.Integer, sa.ForeignKey('grupos.id'), primary_key=True)
)