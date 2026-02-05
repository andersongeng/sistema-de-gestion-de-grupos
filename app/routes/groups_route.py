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
def agregar_estudiantes_grupo(id: int):
	# Accept JSON: {"estudiantes": [{"nombre":"","apellido":"","cedula":123}, ...]}
	# Or single estudiante object: {"estudiante": { ... }}
	# Or form data for a single estudiante: nombre, apellido, cedula
	try:
		from app.models.estudiante import Estudiante
	except Exception:
		return jsonify({"error": "Estudiante model not available"}), 501

	grupo = Grupo.query.get(id)
	if grupo is None:
		return jsonify({"error": "Grupo not found"}), 404

	# Parse incoming estudiantes
	estudiantes_payload = []
	if request.is_json:
		data = request.get_json() or {}
		if 'estudiantes' in data and isinstance(data.get('estudiantes'), list):
			estudiantes_payload = data.get('estudiantes')
		elif 'estudiante' in data and isinstance(data.get('estudiante'), dict):
			estudiantes_payload = [data.get('estudiante')]
		else:
			# maybe user passed a single estudiante object directly
			if isinstance(data, dict) and any(k in data for k in ('nombre','apellido','cedula')):
				estudiantes_payload = [data]
	else:
		# form data: expect nombre, apellido, cedula for a single estudiante
		nombre = request.form.get('nombre')
		apellido = request.form.get('apellido')
		cedula = request.form.get('cedula')
		if nombre or apellido or cedula:
			estudiantes_payload = [{ 'nombre': nombre, 'apellido': apellido, 'cedula': cedula }]

	if not estudiantes_payload:
		return jsonify({"error": "No estudiantes provided"}), 400

	added = []
	created = []
	missing = []
	conflicts = []

	# First pass: find or create Estudiante objects, collect them
	est_objects = []
	for item in estudiantes_payload:
		if not isinstance(item, dict):
			continue
		nombre = item.get('nombre')
		apellido = item.get('apellido')
		cedula = item.get('cedula')

		# cedula is required to uniquely identify
		try:
			cedula_int = int(cedula)
		except Exception:
			cedula_int = None

		est_obj = None
		if cedula_int is not None:
			est_obj = Estudiante.query.filter_by(cedula=cedula_int).first()

		if not est_obj:
			# create if not exists — try to use create() if provided
			if nombre and apellido and cedula_int is not None and hasattr(Estudiante, 'create'):
				try:
					est_obj = Estudiante.create(nombre=nombre, apellido=apellido, cedula=cedula_int)
					created.append(cedula_int)
				except Exception:
					est_obj = None
			if not est_obj and nombre and apellido and cedula_int is not None:
				# manual create
				est_obj = Estudiante(nombre=nombre, apellido=apellido, cedula=cedula_int)
				db.session.add(est_obj)
				# flush so the new Estudiante has an identity for relationship inserts
				db.session.flush()
				created.append(cedula_int)
			elif not est_obj:
				# cannot create without required fields
				missing.append(cedula if cedula is not None else {'item': item})

		if est_obj:
			est_objects.append(est_obj)

	# Detect conflicts: students that belong to groups in other evaluaciones
	# We must check conflicts considering ALL students (existing + new) to ensure
	# no pair has worked together in a previous evaluation.
	all_check_students = list(grupo.estudiantes) + est_objects
	if all_check_students:
		detected = grupo.find_conflicts_in_other_evaluaciones(all_check_students)
		# Note: do NOT clear `detected` for subset matches. Any existing group in another
		# evaluation that includes these students will be treated as a conflict. In
		# particular, exact matches (same set of students) should also be blocked.
		# Build a map of external group -> submitted cedulas that are members of that external group.
		# We will only treat as conflicts those situations where:
		#  - the external group belongs to the same evaluation (always conflict for those students), or
		#  - the external group contains two or more of the submitted students (they previously worked together)
		conflicted_cedulas = set()
		existing_group_map = {}
		# map cedula -> (nombre, apellido) from detected payload so conflicts can include names
		name_map = { (c.get('cedula')): (c.get('nombre'), c.get('apellido')) for c in detected }
		for c in detected:
			ced = c.get('cedula')
			for eg in c.get('existing_groups', []):
				gid = eg.get('grupo_id')
				entry = existing_group_map.setdefault(gid, {
					'cedulas': set(),
					'evaluacion_id': eg.get('evaluacion_id'),
					'evaluacion_titulo': eg.get('evaluacion_titulo'),
					'grupo_numero': eg.get('grupo_numero')
				})
				entry['cedulas'].add(ced)

		# Translate groups in the map into conflict entries according to the rules above
		for gid, info in existing_group_map.items():
			cedset = info.get('cedulas', set())
			if not cedset:
				continue
			# same evaluation groups -> block all students
			if info.get('evaluacion_id') == grupo.evaluacion_id:
				for ced in cedset:
					if ced in conflicted_cedulas:
						continue
					conflicted_cedulas.add(ced)
					nombre, apellido = name_map.get(ced) if name_map.get(ced) else (None, None)
					conflicts.append({
						'cedula': ced,
						'nombre': nombre,
						'apellido': apellido,
						'existing_group_id': gid,
						'existing_group_numero': info.get('grupo_numero'),
						'evaluacion_titulo': info.get('evaluacion_titulo'),
						'same_evaluacion': True
					})
			# external evaluation: only treat as conflict when two or more submitted students
			# belong to the same external group (they worked together previously)
			elif len(cedset) >= 2:
				for ced in cedset:
					if ced in conflicted_cedulas:
						continue
					conflicted_cedulas.add(ced)
					nombre, apellido = name_map.get(ced) if name_map.get(ced) else (None, None)
					conflicts.append({
						'cedula': ced,
						'nombre': nombre,
						'apellido': apellido,
						'existing_group_id': gid,
						'existing_group_numero': info.get('grupo_numero'),
						'evaluacion_titulo': info.get('evaluacion_titulo'),
						'same_evaluacion': False
					})

		# Also detect conflicts where a student already belongs to a DIFFERENT group
		# within the SAME evaluation — these should be blocked as well.
		for est_obj in est_objects:
			ced = getattr(est_obj, 'cedula', None)
			if ced is None or ced in conflicted_cedulas:
				continue
			# find groups for this estudiante that are in the same evaluation but not this group
			other_same_eval = [g for g in getattr(est_obj, 'grupos', []) if getattr(g, 'evaluacion_id', None) == grupo.evaluacion_id and getattr(g, 'id', None) != getattr(grupo, 'id', None)]
			if other_same_eval:
				conflicted_cedulas.add(ced)
				conflicts.append({
					'cedula': ced,
					'nombre': getattr(est_obj, 'nombre', None),
					'apellido': getattr(est_obj, 'apellido', None),
					'existing_group_id': other_same_eval[0].id,
					'existing_group_numero': other_same_eval[0].numero,
					'evaluacion_titulo': getattr(getattr(other_same_eval[0], 'evaluation', None), 'titulo', None),
					'same_evaluacion': True
				})

	# Second pass: append non-conflicted estudiantes to the grupo
	for est_obj in est_objects:
		ced = getattr(est_obj, 'cedula', None)
		if ced in [None]:
			continue
		if ced in [c.get('cedula') for c in conflicts]:
			continue
		if est_obj not in grupo.estudiantes:
			grupo.estudiantes.append(est_obj)
			added.append(ced)

	# commit changes
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		return jsonify({"error": "DB error", "detail": str(e)}), 500

	return jsonify({"added": added, "created": created, "missing": missing, "conflicts": conflicts, "total_in_group": len(grupo.estudiantes)}), 200


@groups_bp.route('/grupos/<int:id>', methods=['GET'])
def detalle_grupo(id: int):
	"""Render a page showing a specific grupo and its estudiantes."""
	grupo = Grupo.query.get_or_404(id)
	from flask import render_template
	return render_template('grupos/detalle_grupo.html', grupo=grupo)


@groups_bp.route('/grupos/<int:id>', methods=['DELETE'])
def eliminar_grupo(id: int):
	"""Delete a Grupo and its enrollments.

	Returns JSON `{"deleted": <id>}` on success, or an error object.
	"""
	grupo = Grupo.query.get(id)
	if grupo is None:
		return jsonify({"error": "Grupo not found"}), 404

	try:
		db.session.delete(grupo)
		db.session.commit()
		return jsonify({"deleted": id}), 200
	except Exception as e:
		db.session.rollback()
		return jsonify({"error": "DB error", "detail": str(e)}), 500