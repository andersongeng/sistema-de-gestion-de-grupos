def test_post_evaluacion_route(client):
    # 1. Crear el registro

    evaluacion_titulo = "Evaluacion 1"

    # 2. Enviar una solicitud POST al endpoint de evaluaciones
    response = client.post('/evaluaciones', json={
        'titulo': evaluacion_titulo
    })

    # 3. Verificar que la respuesta sea exitosa
    assert response.status_code == 200

    # 4. Verificar que se haya creado la evaluacion
    evaluacion_db = response.get_json()
    assert evaluacion_db['titulo'] == evaluacion_titulo
    assert evaluacion_db['id'] is not None