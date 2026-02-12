import json
import logging

from fastapi.testclient import TestClient

from cyberYJ.api.http_app import create_app


def test_post_interpret_success():
    client = TestClient(create_app(api_key="test-key", rate_limit_max=10, rate_limit_window_seconds=60))
    resp = client.post(
        "/v1/divination/interpret",
        headers={"X-API-Key": "test-key", "X-Request-ID": "req-success-001"},
        json={"coins": [6, 7, 8, 9, 7, 7]},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "hexagram" in body
    assert "analysis" in body
    assert resp.headers["X-Request-ID"] == "req-success-001"


def test_post_interpret_invalid_input():
    client = TestClient(create_app(api_key="test-key", rate_limit_max=10, rate_limit_window_seconds=60))
    resp = client.post(
        "/v1/divination/interpret",
        headers={"X-API-Key": "test-key"},
        json={"coins": [6, 7]},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_INPUT"
    assert "request_id" in resp.json()["error"]
    assert resp.headers.get("X-Request-ID")


def test_post_interpret_missing_api_key():
    app = create_app(api_key="test-key", rate_limit_max=10, rate_limit_window_seconds=60)
    client = TestClient(app)
    resp = client.post("/v1/divination/interpret", json={"coins": [6, 7, 8, 9, 7, 7]})
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"
    assert "request_id" in resp.json()["error"]
    assert resp.headers.get("X-Request-ID")
    assert app.state.error_tracker.snapshot()["UNAUTHORIZED"] == 1


def test_post_interpret_rate_limited():
    app = create_app(api_key="test-key", rate_limit_max=1, rate_limit_window_seconds=60)
    client = TestClient(app)
    headers = {"X-API-Key": "test-key"}
    first = client.post("/v1/divination/interpret", headers=headers, json={"coins": [6, 7, 8, 9, 7, 7]})
    second = client.post("/v1/divination/interpret", headers=headers, json={"coins": [6, 7, 8, 9, 7, 7]})

    assert first.status_code == 200
    assert second.status_code == 429
    body = second.json()
    assert body["error"]["code"] == "RATE_LIMITED"
    assert "request_id" in body["error"]
    assert second.headers.get("Retry-After")
    assert second.headers.get("X-Request-ID")
    assert app.state.error_tracker.snapshot()["RATE_LIMITED"] == 1


def test_structured_log_contains_request_completed_event(caplog):
    app = create_app(api_key="test-key", rate_limit_max=10, rate_limit_window_seconds=60)
    client = TestClient(app)
    caplog.set_level(logging.INFO, logger="cyberyj-http-api")

    req_id = "req-log-001"
    resp = client.post(
        "/v1/divination/interpret",
        headers={"X-API-Key": "test-key", "X-Request-ID": req_id},
        json={"coins": [6, 7, 8, 9, 7, 7]},
    )

    assert resp.status_code == 200

    events = []
    for record in caplog.records:
        try:
            payload = json.loads(record.getMessage())
            events.append(payload)
        except Exception:
            continue

    assert any(
        event.get("event") == "request.completed"
        and event.get("request_id") == req_id
        and event.get("status_code") == 200
        for event in events
    )
