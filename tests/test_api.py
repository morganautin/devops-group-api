from fastapi.testclient import TestClient
from src.main import app, tasks


client = TestClient(app)


def setup_function():
    tasks.clear()


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Préparer le projet DevOps",
            "description": "Créer une API REST pour le pipeline CI/CD",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Préparer le projet DevOps"
    assert data["done"] is False


def test_list_tasks():
    client.post("/tasks", json={"title": "Premier test"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_task_without_title_fails():
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 400
