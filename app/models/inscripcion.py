import sqlalchemy as sa
from app.extensions import db

inscripciones = db.Table(
    'inscripciones',
    sa.Column('id', sa.ForeignKey('estudiantes.id'), primary_key=True),
    sa.Column('id', sa.ForeignKey('grupos.id'), primary_key=True)
)