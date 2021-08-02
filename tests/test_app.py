from fastapi.testclient import TestClient

from wallet_service.app import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        '/v1/users',
        json={'username': 'test'}
    )
    assert response.status_code == 201
    # assert response.json() == {"msg": "msg"}
