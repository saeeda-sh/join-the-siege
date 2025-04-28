from io import BytesIO

import pytest
from src.app import allowed_file, flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("file.pdf", True),
        ("file.png", True),
        ("file.jpg", True),
        ("file.txt", True),
        ("file", False),
    ],
)
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected


def test_no_file_in_request(client):
    response = client.post("/classify_file")
    assert response.status_code == 400


def test_no_selected_file(client):
    data = {"file": (BytesIO(b""), "")}  # Empty filename
    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
