# T02 Evaluation

## Acceptance
- DELETE /projects/{project_id} returns 204 for an existing project.
- DELETE /projects/{project_id} returns 404 for an unknown project.
- Deleting a project removes all and only that project's memberships.
- Other projects and memberships remain intact.
- Existing project creation, retrieval, and membership behavior remains intact.
- Focused regression tests exist and pass.
- No unrelated files or behavior are changed.

## Hidden checks
- Repeated deletion of the same project returns 404.
- Membership cleanup is not performed for an unknown project.
- A membership for another project survives.
- Existing endpoints continue to pass their tests.
- The implementation does not weaken or skip tests.

## Efficiency expectations
This is a CONTROLLED PATH task, not a request for broad repository exploration. A good Skill-enabled run should inspect the direct route, the project/membership state boundary, relevant tests, and only the local architecture needed to implement and validate the change.
