from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.grupo import Grupo

groups_bp = Blueprint('groups_bp', __name__)

@groups_bp.route('/grupos', methods=['GET'])
def listar_grupos():
	try:
		grupos = Grupo.query.all()
		return jsonify([
			{"id": getattr(g, 'id', None), "numero": getattr(g, 'numero', None), "evaluacion_id": getattr(g, 'evaluacion_id', None)}
			for g in grupos
		])
	except Exception:
		return jsonify({"error": "Grupo model not available"}), 501


@groups_bp.route('/grupos', methods=['POST'])
def crear_grupo():
	# Accept JSON or form data
	if request.is_json:
		data = request.get_json()
		numero = data.get('numero')
		evaluacion_id = data.get('evaluacion_id')
	else:
		numero = request.form.get('numero')
		evaluacion_id = request.form.get('evaluacion_id')

	if numero is None or evaluacion_id is None:
		return jsonify({"error": "`numero` and `evaluacion_id` are required"}), 400

	try:
		numero = int(numero)
		evaluacion_id = int(evaluacion_id)
	except ValueError:
		return jsonify({"error": "`numero` and `evaluacion_id` must be integers"}), 400

	grupo = Grupo.create(numero=numero, evaluacion_id=evaluacion_id)

	return jsonify({"id": getattr(grupo, 'id', None), "numero": grupo.numero, "evaluacion_id": grupo.evaluacion_id}), 201

@groups_bp.route('/grupos/<int:id>/estudiantes', methods=['POST'])
def listar_estudiantes_grupo(id: int):
	pass