from fastapi.testclient import TestClient

from cyberYJ.api.http_app import create_app


def test_post_interpret_success():
    client = TestClient(create_app())
    resp = client.post("/v1/divination/interpret", json={"coins": [6, 7, 8, 9, 7, 7]})
    assert resp.status_code == 200
    body = resp.json()
    assert "hexagram" in body
    assert "analysis" in body


def test_post_interpret_invalid_input():
    client = TestClient(create_app())
    resp = client.post("/v1/divination/interpret", json={"coins": [6, 7]})
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_INPUT"
