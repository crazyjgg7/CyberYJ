from fastapi.testclient import TestClient

from cyberYJ.api.http_app import create_app


def test_post_interpret_success():
    client = TestClient(create_app(api_key="test-key", rate_limit_max=10, rate_limit_window_seconds=60))
    resp = client.post(
        "/v1/divination/interpret",
        headers={"X-API-Key": "test-key"},
        json={"coins": [6, 7, 8, 9, 7, 7]},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "hexagram" in body
    assert "analysis" in body


def test_post_interpret_invalid_input():
    client = TestClient(create_app(api_key="test-key", rate_limit_max=10, rate_limit_window_seconds=60))
    resp = client.post(
        "/v1/divination/interpret",
        headers={"X-API-Key": "test-key"},
        json={"coins": [6, 7]},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_INPUT"


def test_post_interpret_missing_api_key():
    client = TestClient(create_app(api_key="test-key", rate_limit_max=10, rate_limit_window_seconds=60))
    resp = client.post("/v1/divination/interpret", json={"coins": [6, 7, 8, 9, 7, 7]})
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"


def test_post_interpret_rate_limited():
    client = TestClient(create_app(api_key="test-key", rate_limit_max=1, rate_limit_window_seconds=60))
    headers = {"X-API-Key": "test-key"}
    first = client.post("/v1/divination/interpret", headers=headers, json={"coins": [6, 7, 8, 9, 7, 7]})
    second = client.post("/v1/divination/interpret", headers=headers, json={"coins": [6, 7, 8, 9, 7, 7]})

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.json()["error"]["code"] == "RATE_LIMITED"
