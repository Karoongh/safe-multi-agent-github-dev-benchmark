from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def upload(tmp_path, monkeypatch, filename, content, content_type="application/octet-stream"):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    return client.post(
        "/upload",
        files={"file": (filename, content, content_type)},
    )


def test_upload_text_file(tmp_path, monkeypatch):
    response = upload(tmp_path, monkeypatch, "hello.txt", b"hello world", "text/plain")

    assert response.status_code == 200
    assert response.json()["filename"] == "hello.txt"
    assert response.json()["size"] == 11
    assert (tmp_path / "hello.txt").read_bytes() == b"hello world"


def test_rejects_unsupported_extension(tmp_path, monkeypatch):
    response = upload(tmp_path, monkeypatch, "script.exe", b"MZ")
    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_rejects_content_that_does_not_match_extension(tmp_path, monkeypatch):
    response = upload(tmp_path, monkeypatch, "image.png", b"not a png")
    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_rejects_invalid_utf8_text(tmp_path, monkeypatch):
    response = upload(tmp_path, monkeypatch, "bad.txt", b"\xff\xfe")
    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_sanitizes_path_traversal(tmp_path, monkeypatch):
    response = upload(tmp_path, monkeypatch, "../../hello.txt", b"safe")
    assert response.status_code == 200
    assert response.json()["filename"] == "hello.txt"
    assert (tmp_path / "hello.txt").read_bytes() == b"safe"
    assert not (tmp_path.parent / "hello.txt").exists()


def test_duplicate_filename_does_not_overwrite(tmp_path, monkeypatch):
    first = upload(tmp_path, monkeypatch, "same.txt", b"first")
    second = upload(tmp_path, monkeypatch, "same.txt", b"second")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["filename"] != second.json()["filename"]
    assert (tmp_path / first.json()["filename"]).read_bytes() == b"first"
    assert (tmp_path / second.json()["filename"]).read_bytes() == b"second"


def test_rejects_file_over_size_limit_and_removes_partial_file(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    monkeypatch.setattr(main, "MAX_UPLOAD_SIZE", 4)

    response = client.post(
        "/upload",
        files={"file": ("large.txt", b"12345", "text/plain")},
    )

    assert response.status_code == 413
    assert list(tmp_path.iterdir()) == []


def test_accepts_pdf_with_matching_signature(tmp_path, monkeypatch):
    content = b"%PDF-1.7\nexample"
    response = upload(tmp_path, monkeypatch, "report.pdf", content, "text/plain")

    assert response.status_code == 200
    assert response.json()["content_type"] == "application/pdf"
    assert (tmp_path / "report.pdf").read_bytes() == content


def test_rejects_empty_or_dot_filename(tmp_path, monkeypatch):
    response = upload(tmp_path, monkeypatch, "..", b"content")
    assert response.status_code == 400
    assert list(tmp_path.iterdir()) == []
