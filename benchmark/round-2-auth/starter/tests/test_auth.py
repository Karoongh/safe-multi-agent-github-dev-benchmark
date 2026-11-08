import sys
from pathlib import Path

from fastapi.testclient import TestClient

FIXTURE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIXTURE_ROOT))

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health_is_public():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_admin_report_response_shape_with_current_fallback(monkeypatch):
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)

    response = client.get("/admin/report", headers={"X-API-Key": "dev-secret"})

    assert response.status_code == 200
    assert response.json() == {
        "report": {
            "active_users": 42,
            "revenue_cents": 125000,
        }
    }
