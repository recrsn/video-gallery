def test_index(client):
    response = client.get('/')

    assert response.content_type == 'application/json'
    assert response.status == '200 OK'
    assert response.json == {'message': 'OK'}
