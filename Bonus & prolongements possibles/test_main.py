
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_personnage():
    response = client.post("/personnages", json={"nom": "Harry Potter", "score": 90})
    assert response.status_code == 200
    assert response.json() == {"nom": "Harry Potter", "score": 90, "niveau": "Fort"}

def test_get_personnage():
    response = client.get("/personnages/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "nom": "Harry Potter", "score": 90, "niveau": "Fort"}
