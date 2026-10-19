from datetime import datetime, timezone
import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException
from app.schemas.response import ErrorResponse

logger = logging.getLogger("uvicorn.error")


def create_error_response(
    status_code: int,
    error_code: str,
    message: str,
    errors: list | None = None,
) -> JSONResponse:
    payload = ErrorResponse(
        success=False,
        statusCode=status_code,
        timestamp=datetime.now(timezone.utc).isoformat(),
        errorCode=error_code,
        message=message,
        errors=errors,
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(exclude_none=True),
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(
            f"[{request.method}] {request.url.path} -> {exc.status_code} {exc.error_code}: {exc.message}"
        )
        return create_error_response(
            status_code=exc.status_code,
            error_code=exc.error_code,
            message=exc.message,
            errors=exc.errors,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        formatted_errors = []
        for error in exc.errors():
            loc = " -> ".join(str(loc_part) for loc_part in error.get("loc", []))
            formatted_errors.append(f"{loc}: {error.get('msg')}")

        first_msg = formatted_errors[0] if formatted_errors else "Dữ liệu không hợp lệ"

        logger.warning(
            f"[{request.method}] {request.url.path} -> 400 VALIDATION_ERROR: {first_msg}"
        )
        return create_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            message=first_msg,
            errors=formatted_errors,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        error_code = "HTTP_ERROR"
        if exc.status_code == 404:
            error_code = "NOT_FOUND"
        elif exc.status_code == 405:
            error_code = "METHOD_NOT_ALLOWED"

        logger.warning(
            f"[{request.method}] {request.url.path} -> {exc.status_code} {error_code}: {exc.detail}"
        )
        return create_error_response(
            status_code=exc.status_code,
            error_code=error_code,
            message=str(exc.detail),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(
            f"[Unhandled Error] [{request.method}] {request.url.path} -> {str(exc)}",
            exc_info=True,
        )
        return create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
            message="Lỗi hệ thống không mong muốn",
        )
