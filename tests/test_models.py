from app.extensions import db
from app.models.estudiante import Estudiante
from app.models.grupo import Grupo

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

def test_crear_grupo(app):
    """
    Prueba que un grupo se guarda correctamente en la base de datos.
    El argumento 'app' viene de el fixture en conftest.py
    """

    # 1. Crear el registro
    nuevo_grupo = Grupo(
        numero=1
    )

    # 2. Abrir el contexto de la base de datos para operar
    with app.app_context():
        db.session.add(nuevo_grupo)
        db.session.commit()

        # 3. Consultar la base de datos para verificar
        grupo_db = Grupo.query.filter_by(numero=1).first()

        # 4. Afirmaciones
        assert grupo_db is not None
        assert grupo_db.numero == 1
        assert grupo_db.id is not None

def test_crear_inscripcion(app):
    """
    Prueba que se puedan inscribir estudiantes en un grupo
    y guardarse correctamente en la base de datos.
    El argumento 'app' viene de el fixture en conftest.py
    """
    # 1. Crear los registros
    estudiante_1 = Estudiante(
        nombre="Anderson",
        apellido="Granado",
        cedula=1
    )

    estudiante_2 = Estudiante(
        nombre="Fulano",
        apellido="Fulanito",
        cedula=2
    )

    nuevo_grupo = Grupo(
        numero=1
    )

    # 2. Abrir el contexto de la base de datos para operar
    with app.app_context():
        db.session.add_all([estudiante_1, estudiante_2, nuevo_grupo])
        db.session.commit()

        # 3. Inscribir usando .append()

        nuevo_grupo.estudiantes.append(estudiante_1)
        nuevo_grupo.estudiantes.append(estudiante_2)
        db.session.commit()

        # 4. Verificacion de ida: Grupo tiene a los estudiantes
        assert len(nuevo_grupo.estudiantes) == 2
        assert estudiante_1 in nuevo_grupo.estudiantes
        assert estudiante_2 in nuevo_grupo.estudiantes

        # 5. Verificacion de vuelta: El estudiante sabe en que grupo esta
        assert len(estudiante_1.grupos) == 1
        assert nuevo_grupo in estudiante_1.grupos

def test_estudiante_create_method(app):
    """
    Prueba que el metodo crea un nuevo estudiante
    y lo guarda en la base de datos.
    """

    # 1. Datos de prueba

    datos = {
        'nombre': 'Fulano',
        'apellido': 'De Tal',
        'cedula': 123
    }

    # 2. Ejecutar el metodo
    nuevo_estudiante = Estudiante.create(**datos)

    # 3. Verificar que el estudiante fue creado correctamente
    assert nuevo_estudiante is not None
    assert nuevo_estudiante.cedula == 123
    assert nuevo_estudiante.id is not None

    estudiante_db = Estudiante.query.filter_by(cedula=123).first()
    assert estudiante_db is not None
    assert estudiante_db.id == nuevo_estudiante.id