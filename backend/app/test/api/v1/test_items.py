# tests/test_items.py
from fastapi.testclient import TestClient
from app.api.api import app

client = TestClient(app)

def test_create_item():
    response = client.post("/api/v1/items/", json={"title": "Test Item", "description": "Some desc"})
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert "id" in data

def test_get_items():
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
