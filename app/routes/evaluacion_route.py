from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.evaluacion import Evaluacion
from app.extensions import db

evaluacion_bp = Blueprint('evaluacion_bp', __name__)


@evaluacion_bp.route('/evaluaciones', methods=['GET'])
def listar_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    return render_template('evaluaciones/listar_evaluaciones.html', evaluaciones=evaluaciones)


@evaluacion_bp.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    # Support JSON API clients and HTML form submissions
    if request.is_json:
        data = request.get_json()
        titulo_nueva_evaluacion = data.get('titulo')
    else:
        titulo_nueva_evaluacion = request.form.get('titulo')

    nueva_evaluacion = Evaluacion.create(titulo=titulo_nueva_evaluacion)

    # Redirect to the listing page after creation
    return redirect(url_for('evaluacion_bp.listar_evaluaciones'))


@evaluacion_bp.route('/evaluaciones/<int:id>', methods=['GET'])
def detalle_evaluacion(id: int):
    """Mostrar una evaluación específica y sus grupos."""
    evaluacion = Evaluacion.query.get(id)
    return render_template('evaluaciones/detalle_evaluacion.html', evaluacion=evaluacion)


@evaluacion_bp.route('/evaluaciones/<int:id>', methods=['DELETE'])
def eliminar_evaluacion(id: int):
    """Delete an Evaluacion and return JSON result.

    Note: this will attempt to delete the evaluation record. If there are
    dependent records (e.g. groups) and the database does not cascade, the
    operation may fail and return a 500 with details.
    """
    evaluacion = Evaluacion.query.get(id)
    if evaluacion is None:
        return jsonify({"error": "Evaluacion not found"}), 404

    try:
        db.session.delete(evaluacion)
        db.session.commit()
        return jsonify({"deleted": id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "DB error", "detail": str(e)}), 500