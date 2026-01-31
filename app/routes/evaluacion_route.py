from flask import Blueprint, request, jsonify
from app.models.evaluacion import Evaluacion

evaluacion_bp = Blueprint('evaluacion_bp', __name__)

@evaluacion_bp.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    data = request.get_json()
    titulo_nueva_evaluacion = data['titulo']

    nueva_evaluacion = Evaluacion.create(titulo=titulo_nueva_evaluacion)
    return {
        'id': nueva_evaluacion.id,
        'titulo': nueva_evaluacion.titulo
    }, 200