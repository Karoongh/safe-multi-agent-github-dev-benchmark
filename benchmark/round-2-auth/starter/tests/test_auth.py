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
    assert "API key" not in response.text


def test_admin_report_fails_closed_when_key_is_blank(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "   ")

    response = client.get("/admin/report", headers={"X-API-Key": "   "})

    assert response.status_code == 503


def test_admin_report_rejects_missing_key(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "benchmark-test-key")

    response = client.get("/admin/report")

    assert response.status_code == 401
    assert "benchmark-test-key" not in response.text


def test_admin_report_rejects_wrong_key(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "benchmark-test-key")

    response = client.get(
        "/admin/report",
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 401
    assert "benchmark-test-key" not in response.text


def test_admin_report_accepts_exact_configured_key(monkeypatch):
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


def test_admin_report_does_not_expose_secret_on_error(monkeypatch):
    secret = "super-secret-benchmark-key"
    monkeypatch.setenv("ADMIN_API_KEY", secret)

    response = client.get(
        "/admin/report",
        headers={"X-API-Key": "incorrect"},
    )

    assert response.status_code == 401
    assert secret not in response.text


def test_authentication_is_not_bypassed_by_another_method(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "benchmark-test-key")

    response = client.post("/admin/report")

    assert response.status_code in {405, 404}
