from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_headers_valid():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
    }
    response = client.get(
        "/headers",
        headers=headers,
    )

    assert response.status_code == 200
