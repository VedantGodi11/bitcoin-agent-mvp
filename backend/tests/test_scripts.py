import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_auth_token():
    unique_id = uuid.uuid4().hex[:8]
    username = f"scriptuser_{unique_id}"
    email = f"{username}@example.com"
    password = "testpass123"

    client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )
    response = client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password
        }
    )
    return response.json()["access_token"]


def test_validate_script():
    token = create_auth_token()
    response = client.post(
        "/api/scripts/validate",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": "OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "is_valid" in data
    assert "errors" in data
    assert "warnings" in data


def test_validate_empty_script():
    token = create_auth_token()
    response = client.post(
        "/api/scripts/validate",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": ""}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
    assert len(data["errors"]) > 0