from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger
import traceback

from app.core.exceptions import (
    FileUploadError,
    FileNotFoundError
)

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler that formats all errors into a standardized response.
    """
    # Handle custom exceptions
    if isinstance(exc, FileUploadError):
        return await handle_file_upload_error(exc)
    if isinstance(exc, FileNotFoundError):
        return await handle_file_not_found_error(exc)

    # Handle FastAPI's built-in validation errors
    if isinstance(exc, RequestValidationError):
        return await handle_validation_error(exc)

    # Handle generic HTTPExceptions (e.g., 404 Not Found)
    if isinstance(exc, HTTPException):
        return await handle_http_exception(exc)

    # Handle all other unexpected errors
    return await handle_unexpected_error(exc)

# --- Helper functions for specific error types ---

async def handle_file_upload_error(exc: FileUploadError) -> JSONResponse:
    logger.error(f"File upload error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_type": "FileUploadError",
            "message": str(exc),
            "details": None
        }
    )

async def handle_file_not_found_error(exc: FileNotFoundError) -> JSONResponse:
    logger.error(f"File not found: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_type": "FileNotFoundError",
            "message": str(exc),
            "details": None
        }
    )

async def handle_validation_error(exc: RequestValidationError) -> JSONResponse:
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_type": "ValidationError",
            "message": "Invalid request payload",
            "details": exc.errors()
        }
    )

async def handle_http_exception(exc: HTTPException) -> JSONResponse:
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_type": "HTTPError",
            "message": exc.detail,
            "details": None
        }
    )

async def handle_unexpected_error(exc: Exception) -> JSONResponse:
    logger.critical(f"Unexpected error: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_type": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": None
        }
    )