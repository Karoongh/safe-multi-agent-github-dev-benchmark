class MembershipStore:
    def __init__(self):
        self._items = {}
        self._next_id = 1

    def add(self, project_id: int, user_id: int) -> int:
        membership_id = self._next_id
        self._next_id += 1
        self._items[membership_id] = {
            "id": membership_id,
            "project_id": project_id,
            "user_id": user_id,
        }
        return membership_id

    def for_project(self, project_id: int):
        return [item for item in self._items.values() if item["project_id"] == project_id]

    def delete_for_project(self, project_id: int) -> int:
        ids = [mid for mid, item in self._items.items() if item["project_id"] == project_id]
        for membership_id in ids:
            del self._items[membership_id]
        return len(ids)


memberships = MembershipStore()
