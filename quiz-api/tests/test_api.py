import sys
import os
import pytest

# Ajouter le dossier parent au PYTHONPATH AVANT l'import de app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data


def test_login_wrong_password(client):
    response = client.post("/login", json={
        "password": "wrongpassword"
    })
    assert response.status_code == 401
