"""
FastAPI app for Wechat mini-program integration.
"""

import os
import threading
import time
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


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


def create_app(
    api_key: Optional[str] = None,
    rate_limit_max: Optional[int] = None,
    rate_limit_window_seconds: Optional[int] = None,
) -> FastAPI:
    app = FastAPI(title="CyberYJ Wechat API", version="1.0.0")
    service = DivinationService()
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
        if request.url.path.startswith("/v1/"):
            provided_api_key = request.headers.get("X-API-Key")
            if expected_api_key and provided_api_key != expected_api_key:
                return _error_response(
                    status_code=401,
                    code="UNAUTHORIZED",
                    message="missing or invalid X-API-Key",
                )

            client_host = request.client.host if request.client else "unknown"
            client_id = f"{provided_api_key or 'no-key'}:{client_host}"
            allowed, remaining, reset_in = rate_limiter.allow(client_id)
            if not allowed:
                response = _error_response(
                    status_code=429,
                    code="RATE_LIMITED",
                    message=f"rate limit exceeded, retry in {reset_in}s",
                )
                response.headers["Retry-After"] = str(reset_in)
                response.headers["X-RateLimit-Limit"] = str(effective_rate_limit_max)
                response.headers["X-RateLimit-Remaining"] = "0"
                return response

            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(effective_rate_limit_max)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_in)
            return response

        return await call_next(request)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        _ = request
        _ = exc
        return _error_response(
            status_code=400,
            code="INVALID_INPUT",
            message="coins数组必须包含6个元素 (6/7/8/9)",
        )

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
        _ = request
        return _error_response(status_code=400, code="INVALID_INPUT", message=str(exc))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        _ = request
        return _error_response(status_code=500, code="INTERNAL_ERROR", message=str(exc))

    @app.post("/v1/divination/interpret")
    async def interpret(req: DivinationRequest) -> dict:
        return service.interpret(req.coins, req.question)

    return app
