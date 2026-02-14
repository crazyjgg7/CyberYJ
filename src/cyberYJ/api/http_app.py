"""
FastAPI app for Wechat mini-program integration.
"""

import json
import logging
import os
import threading
import time
import uuid
from typing import Dict, Optional, Tuple

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from cyberYJ.api.divination_service import DivinationService
from cyberYJ.api.models import DivinationRequest


class FixedWindowRateLimiter:
    """Simple in-memory fixed-window limiter keyed by client id."""

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._buckets: Dict[str, Tuple[int, float]] = {}
        self._lock = threading.Lock()

    def allow(self, client_id: str) -> Tuple[bool, int, int]:
        now = time.time()
        with self._lock:
            count, window_start = self._buckets.get(client_id, (0, now))
            elapsed = now - window_start
            if elapsed >= self._window_seconds:
                count = 0
                window_start = now
                elapsed = 0

            if count >= self._max_requests:
                reset_in = max(1, int(self._window_seconds - elapsed))
                return False, 0, reset_in

            count += 1
            self._buckets[client_id] = (count, window_start)
            remaining = max(0, self._max_requests - count)
            reset_in = max(1, int(self._window_seconds - elapsed))
            return True, remaining, reset_in


class ErrorTracker:
    """In-memory error tracker for quick observability."""

    def __init__(self) -> None:
        self._counts: Dict[str, int] = {}
        self._lock = threading.Lock()

    def record(self, code: str) -> None:
        with self._lock:
            self._counts[code] = self._counts.get(code, 0) + 1

    def snapshot(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._counts)


def _resolve_request_id(request: Request) -> str:
    request_id = (request.headers.get("X-Request-ID") or "").strip()
    if request_id:
        return request_id[:128]
    return uuid.uuid4().hex


def _get_request_id(request: Request) -> str:
    request_id = getattr(request.state, "request_id", None)
    if isinstance(request_id, str) and request_id:
        return request_id
    return _resolve_request_id(request)


def _log_structured(logger: logging.Logger, level: int, event: str, **kwargs: object) -> None:
    payload = {"event": event, "timestamp_ms": int(time.time() * 1000)}
    payload.update(kwargs)
    logger.log(level, json.dumps(payload, ensure_ascii=False))


def _error_response(
    status_code: int,
    code: str,
    message: str,
    request_id: Optional[str] = None,
) -> JSONResponse:
    error = {"code": code, "message": message}
    if request_id:
        error["request_id"] = request_id
    return JSONResponse(
        status_code=status_code,
        content={"error": error},
    )


def _validation_message(exc: RequestValidationError) -> str:
    errors = exc.errors()
    if not errors:
        return "请求参数校验失败"

    first = errors[0]
    loc = [str(item) for item in first.get("loc", []) if str(item) != "body"]
    if "coins" in loc:
        return "coins数组必须包含6个元素 (6/7/8/9)"
    if "scene_type" in loc:
        return (
            "scene_type 无效，必须是 fortune/career/love/wealth/health/"
            "study/family/travel/lawsuit 之一"
        )

    message = first.get("msg")
    if isinstance(message, str) and message.strip():
        if loc:
            return f"{'.'.join(loc)}: {message}"
        return message
    return "请求参数校验失败"


def create_app(
    api_key: Optional[str] = None,
    rate_limit_max: Optional[int] = None,
    rate_limit_window_seconds: Optional[int] = None,
) -> FastAPI:
    app = FastAPI(title="CyberYJ Wechat API", version="1.0.0")
    service = DivinationService()
    logger = logging.getLogger("cyberyj-http-api")
    error_tracker = ErrorTracker()
    app.state.error_tracker = error_tracker
    expected_api_key = (
        api_key if api_key is not None else os.getenv("CYBERYJ_API_KEY", "cyberyj-dev-key")
    )
    effective_rate_limit_max = (
        rate_limit_max
        if rate_limit_max is not None
        else int(os.getenv("CYBERYJ_RATE_LIMIT_MAX", "60"))
    )
    effective_rate_limit_window_seconds = (
        rate_limit_window_seconds
        if rate_limit_window_seconds is not None
        else int(os.getenv("CYBERYJ_RATE_LIMIT_WINDOW_SECONDS", "60"))
    )
    rate_limiter = FixedWindowRateLimiter(
        max_requests=max(1, effective_rate_limit_max),
        window_seconds=max(1, effective_rate_limit_window_seconds),
    )

    @app.middleware("http")
    async def auth_and_rate_limit(request: Request, call_next):  # type: ignore[no-untyped-def]
        request_id = _resolve_request_id(request)
        request.state.request_id = request_id
        request_started_at = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"

        _log_structured(
            logger,
            logging.INFO,
            "request.received",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=client_host,
        )

        if request.url.path.startswith("/v1/"):
            provided_api_key = request.headers.get("X-API-Key")
            if expected_api_key and provided_api_key != expected_api_key:
                error_tracker.record("UNAUTHORIZED")
                response = _error_response(
                    status_code=401,
                    code="UNAUTHORIZED",
                    message="missing or invalid X-API-Key",
                    request_id=request_id,
                )
                response.headers["X-Request-ID"] = request_id
                _log_structured(
                    logger,
                    logging.WARNING,
                    "request.rejected",
                    request_id=request_id,
                    method=request.method,
                    path=request.url.path,
                    status_code=401,
                    error_code="UNAUTHORIZED",
                    client_ip=client_host,
                )
                return response

            client_id = f"{provided_api_key or 'no-key'}:{client_host}"
            allowed, remaining, reset_in = rate_limiter.allow(client_id)
            if not allowed:
                error_tracker.record("RATE_LIMITED")
                response = _error_response(
                    status_code=429,
                    code="RATE_LIMITED",
                    message=f"rate limit exceeded, retry in {reset_in}s",
                    request_id=request_id,
                )
                response.headers["Retry-After"] = str(reset_in)
                response.headers["X-RateLimit-Limit"] = str(effective_rate_limit_max)
                response.headers["X-RateLimit-Remaining"] = "0"
                response.headers["X-Request-ID"] = request_id
                _log_structured(
                    logger,
                    logging.WARNING,
                    "request.rejected",
                    request_id=request_id,
                    method=request.method,
                    path=request.url.path,
                    status_code=429,
                    error_code="RATE_LIMITED",
                    client_ip=client_host,
                )
                return response

            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(effective_rate_limit_max)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_in)
            response.headers["X-Request-ID"] = request_id
            duration_ms = int((time.perf_counter() - request_started_at) * 1000)
            _log_structured(
                logger,
                logging.INFO,
                "request.completed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                client_ip=client_host,
            )
            return response

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        duration_ms = int((time.perf_counter() - request_started_at) * 1000)
        _log_structured(
            logger,
            logging.INFO,
            "request.completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            client_ip=client_host,
        )
        return response

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        request_id = _get_request_id(request)
        error_tracker.record("INVALID_INPUT")
        message = _validation_message(exc)
        _log_structured(
            logger,
            logging.WARNING,
            "request.error",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=400,
            error_code="INVALID_INPUT",
        )
        response = _error_response(
            status_code=400,
            code="INVALID_INPUT",
            message=message,
            request_id=request_id,
        )
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
        request_id = _get_request_id(request)
        error_tracker.record("INVALID_INPUT")
        _log_structured(
            logger,
            logging.WARNING,
            "request.error",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=400,
            error_code="INVALID_INPUT",
            detail=str(exc),
        )
        response = _error_response(
            status_code=400,
            code="INVALID_INPUT",
            message=str(exc),
            request_id=request_id,
        )
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        request_id = _get_request_id(request)
        error_tracker.record("INTERNAL_ERROR")
        _log_structured(
            logger,
            logging.ERROR,
            "request.error",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=500,
            error_code="INTERNAL_ERROR",
            exception_type=type(exc).__name__,
            detail=str(exc),
        )
        response = _error_response(
            status_code=500,
            code="INTERNAL_ERROR",
            message=str(exc),
            request_id=request_id,
        )
        response.headers["X-Request-ID"] = request_id
        return response

    @app.post("/v1/divination/interpret")
    @app.post("/v1/learning/interpret")
    async def interpret(req: DivinationRequest) -> dict:
        return service.interpret(req.coins, req.question, req.scene_type)

    return app
