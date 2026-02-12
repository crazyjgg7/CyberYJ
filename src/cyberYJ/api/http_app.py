"""
FastAPI app for Wechat mini-program integration.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from cyberYJ.api.divination_service import DivinationService
from cyberYJ.api.models import DivinationRequest


def create_app() -> FastAPI:
    app = FastAPI(title="CyberYJ Wechat API", version="1.0.0")
    service = DivinationService()

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        _ = request
        _ = exc
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "coins数组必须包含6个元素 (6/7/8/9)",
                }
            },
        )

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
        _ = request
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "INVALID_INPUT",
                    "message": str(exc),
                }
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        _ = request
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(exc),
                }
            },
        )

    @app.post("/v1/divination/interpret")
    async def interpret(req: DivinationRequest) -> dict:
        return service.interpret(req.coins, req.question)

    return app

