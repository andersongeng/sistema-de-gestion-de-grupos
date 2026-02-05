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

    def find_conflicts_in_other_evaluaciones(self, estudiantes):
        """
        Given an iterable of `Estudiante` instances or cedula values, return a list
        of conflicts for students that already belong to one or more groups in
        other evaluaciones (i.e. with a different `evaluacion_id` than this group).

        Returned list elements are dicts of the form::

            {
                'cedula': <cedula>,
                'estudiante_id': <id or None>,
                'existing_groups': [
                    {'grupo_id': <id>, 'grupo_numero': <numero>, 'evaluacion_id': <evaluacion_id>},
                    ...
                ]
            }

        Notes:
        - `estudiantes` may be a mix of `Estudiante` objects or plain cedula values.
        - The method performs minimal DB queries when cedula values are provided.
        """
        conflicts = []
        # local import to avoid circular import at module load
        from app.models.estudiante import Estudiante

        for s in estudiantes:
            est_obj = None
            # accept Estudiante instance
            if hasattr(s, 'cedula') and hasattr(s, 'id'):
                est_obj = s
            else:
                # treat as cedula-like value
                try:
                    ced = int(s)
                except Exception:
                    ced = None
                if ced is not None:
                    est_obj = Estudiante.query.filter_by(cedula=ced).first()

            if not est_obj:
                # no record found for this identifier; skip (caller can create student first)
                continue

            other_groups = [g for g in est_obj.grupos if g.evaluacion_id != self.evaluacion_id]
            if other_groups:
                conflicts.append({
                    'cedula': getattr(est_obj, 'cedula', None),
                    'estudiante_id': getattr(est_obj, 'id', None),
                    'nombre': getattr(est_obj, 'nombre', None),
                    'apellido': getattr(est_obj, 'apellido', None),
                    'existing_groups': [
                        {
                            'grupo_id': g.id,
                            'grupo_numero': g.numero,
                            'evaluacion_id': g.evaluacion_id,
                            'evaluacion_titulo': getattr(getattr(g, 'evaluation', None), 'titulo', None)
                        }
                        for g in other_groups
                    ]
                })

        return conflicts