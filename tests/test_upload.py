from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_text_file(tmp_path, monkeypatch):
    monkeypatch.setattr("app.main.UPLOAD_DIR", tmp_path)

    response = client.post(
        "/upload",
        files={"file": ("hello.txt", b"hello world", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "hello.txt"
    assert response.json()["size"] == 11
    assert (tmp_path / "hello.txt").read_bytes() == b"hello world"
