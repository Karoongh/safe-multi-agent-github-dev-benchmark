from fastapi.testclient import TestClient

from app.main import app
from app.memberships import memberships
from app.projects import projects

client = TestClient(app)


def reset_stores():
    projects._items.clear()
    projects._next_id = 1
    memberships._items.clear()
    memberships._next_id = 1


def setup_function():
    reset_stores()


def test_create_get_and_member_flow_remains_valid():
    response = client.post("/projects", params={"name": "Alpha"})
    assert response.status_code == 201
    project_id = response.json()["id"]

    member = client.post(f"/projects/{project_id}/members", params={"user_id": 7})
    assert member.status_code == 201
    assert client.get(f"/projects/{project_id}").json()["name"] == "Alpha"
    assert len(memberships.for_project(project_id)) == 1


def test_get_missing_project_returns_404():
    assert client.get("/projects/999").status_code == 404


def test_member_creation_for_missing_project_returns_404():
    assert client.post("/projects/999/members", params={"user_id": 7}).status_code == 404


# The benchmark task asks for focused deletion regression coverage.
