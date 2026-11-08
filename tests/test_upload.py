from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def post_upload(tmp_path, monkeypatch, filename, content, content_type="application/octet-stream"):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    return client.post(
        "/upload",
        files={"file": (filename, content, content_type)},
    )


def test_upload_text_file_preserves_response_and_contents(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "hello.txt", b"hello world", "text/plain")

    assert response.status_code == 200
    assert response.json() == {
        "filename": "hello.txt",
        "size": 11,
        "content_type": "text/plain",
    }
    assert (tmp_path / "hello.txt").read_bytes() == b"hello world"


def test_rejects_unsupported_extension(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "payload.exe", b"MZ")

    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_rejects_mismatched_image_signature(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "image.png", b"not a png", "image/png")

    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_rejects_invalid_utf8_text(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "invalid.txt", b"\xff\xfe", "text/plain")

    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_rejects_null_bytes_in_text(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "binary.txt", b"hello\x00world", "text/plain")

    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_sanitizes_path_traversal(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "../../nested/hello.txt", b"safe")

    assert response.status_code == 200
    assert response.json()["filename"] == "hello.txt"
    assert (tmp_path / "hello.txt").read_bytes() == b"safe"


def test_sanitizes_windows_path_traversal(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, r"..\..\outside\hello.txt", b"safe")

    assert response.status_code == 200
    assert response.json()["filename"] == "hello.txt"


def test_duplicate_names_do_not_overwrite(tmp_path, monkeypatch):
    first = post_upload(tmp_path, monkeypatch, "same.txt", b"first")
    second = post_upload(tmp_path, monkeypatch, "same.txt", b"second")

    assert first.status_code == second.status_code == 200
    first_name = first.json()["filename"]
    second_name = second.json()["filename"]
    assert first_name != second_name
    assert (tmp_path / first_name).read_bytes() == b"first"
    assert (tmp_path / second_name).read_bytes() == b"second"


def test_rejects_oversized_file_and_removes_partial_file(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    monkeypatch.setattr(main, "MAX_UPLOAD_SIZE", 4)

    response = client.post(
        "/upload",
        files={"file": ("large.txt", b"12345", "text/plain")},
    )

    assert response.status_code == 413
    assert list(tmp_path.iterdir()) == []


def test_accepts_pdf_signature_without_trusting_client_mime(tmp_path, monkeypatch):
    content = b"%PDF-1.7\nbenchmark"
    response = post_upload(tmp_path, monkeypatch, "report.pdf", content, "text/plain")

    assert response.status_code == 200
    assert response.json()["content_type"] == "application/pdf"
    assert (tmp_path / "report.pdf").read_bytes() == content


def test_rejects_empty_filename(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "", b"content")

    assert response.status_code == 400
    assert list(tmp_path.iterdir()) == []


def test_rejects_windows_reserved_filename(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "CON.txt", b"content")

    assert response.status_code == 400
    assert list(tmp_path.iterdir()) == []


def test_empty_utf8_text_file_is_allowed(tmp_path, monkeypatch):
    response = post_upload(tmp_path, monkeypatch, "empty.txt", b"")

    assert response.status_code == 200
    assert response.json()["size"] == 0
    assert (tmp_path / "empty.txt").read_bytes() == b""
