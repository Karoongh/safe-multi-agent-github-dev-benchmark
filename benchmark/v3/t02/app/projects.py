class ProjectStore:
    def __init__(self):
        self._items = {}
        self._next_id = 1

    def create(self, name: str) -> int:
        project_id = self._next_id
        self._next_id += 1
        self._items[project_id] = {"id": project_id, "name": name}
        return project_id

    def get(self, project_id: int):
        return self._items.get(project_id)

    def delete(self, project_id: int) -> bool:
        return self._items.pop(project_id, None) is not None


projects = ProjectStore()
