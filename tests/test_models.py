from app.models.estudiante import Estudiante
from app.extensions import db

def test_crear_estudiante(app):
    """
    Prueba que un estudiante se guarda correctamente en la base de datos.
    El argumento 'app' viene de el fixture en conftest.py
    """
    # 1. Crear el registro
    nuevo_estudiante = Estudiante(
        cedula=31131247,
        nombre="Anderson",
        apellido="Granado"
    )

    # 2. Abrir el contexto de la base de datos para operar
    with app.app_context():
        db.session.add(nuevo_estudiante)
        db.session.commit()

        # 3. Consultar la base de datos para verificar
        estudiante_db = Estudiante.query.filter_by(cedula=31131247).first()

    # 4. Afirmaciones
    assert estudiante_db is not None
    assert estudiante_db.nombre == "Anderson"
    assert estudiante_db.id is not None