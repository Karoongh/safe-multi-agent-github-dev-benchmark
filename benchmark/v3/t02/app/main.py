from fastapi import FastAPI, HTTPException, status

from .memberships import memberships
from .projects import projects

app = FastAPI(title="T02 Project API")


@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(name: str):
    project_id = projects.create(name)
    return {"id": project_id, "name": name}


@app.get("/projects/{project_id}")
def get_project(project_id: int):
    project = projects.get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.post("/projects/{project_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(project_id: int, user_id: int):
    if projects.get(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    membership_id = memberships.add(project_id, user_id)
    return {"id": membership_id, "project_id": project_id, "user_id": user_id}


# The deletion behavior is intentionally left for the benchmark task.
