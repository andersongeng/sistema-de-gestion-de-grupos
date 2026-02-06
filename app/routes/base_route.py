from flask import Blueprint, redirect, url_for

# Creamos el Blueprint
base_bp = Blueprint('base', __name__)

@base_bp.route('/')
def index():
    # Redirige a la función 'ver_evaluaciones' del Blueprint 'evaluaciones'
    # El formato es 'nombre_del_blueprint.nombre_de_la_funcion'
    return redirect(url_for('evaluacion_bp.listar_evaluaciones'))

@base_bp.app_errorhandler(404)
def handle_404(e):
    # Captura errores de toda la app y redirige
    return redirect(url_for('evaluacion_bp.listar_evaluaciones'))