import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

FIXTURE_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = FIXTURE_ROOT / "app" / "main.py"
SPEC = importlib.util.spec_from_file_location("round2_auth_app", APP_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
app = MODULE.app

client = TestClient(app)


def test_health_is_public():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_admin_report_fails_closed_when_key_is_missing(monkeypatch):
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)

    response = client.get("/admin/report")

    assert response.status_code == 503


def test_admin_report_fails_closed_when_key_is_blank(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "")

    response = client.get("/admin/report", headers={"X-API-Key": ""})

    assert response.status_code == 503


def test_admin_report_rejects_missing_key(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "benchmark-test-key")

    response = client.get("/admin/report")

    assert response.status_code == 401


def test_admin_report_rejects_wrong_key(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "benchmark-test-key")

    response = client.get(
        "/admin/report",
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 401


def test_admin_report_authorized_response_shape(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "benchmark-test-key")

    response = client.get(
        "/admin/report",
        headers={"X-API-Key": "benchmark-test-key"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "report": {
            "active_users": 42,
            "revenue_cents": 125000,
        }
    }
