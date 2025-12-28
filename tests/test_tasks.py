# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_create_task():
#     response = client.post("/api/tasks/", json={
#         "title": "Test Task",
#         "description": "Test Desc",
#         "due_date": "2025-01-01"
#     })
#     assert response.status_code == 200

# def test_get_tasks():
#     response = client.get("/api/tasks/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)



def test_tasks_with_auth(client):
    login = client.post("/api/auth/login", params={
        "username": "admin",
        "password": "admin"
    })
    token = login.json()["access_token"]

    response = client.get(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_update_task(client, auth_token):
    response = client.put(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"status": "completed"}
    )
    assert response.status_code == 200


def test_delete_task(client, auth_token):
    response = client.delete(
        "/api/tasks/1",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
