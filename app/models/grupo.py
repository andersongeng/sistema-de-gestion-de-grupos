from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column

class Grupo(db.Model):
    __tablename__ = 'grupos'

    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[int] = mapped_column(nullable=False)
    