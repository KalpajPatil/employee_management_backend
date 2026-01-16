import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.core.exceptions import EmployeeNotFoundError, ShiftConflictError

logger = logging.getLogger(__name__)


async def employee_not_found_handler(
    request: Request,
    exc: EmployeeNotFoundError,
) -> JSONResponse:
    logger.warning(
        "EmployeeNotFoundError on %s %s: %s",
        request.method,
        request.url,
        exc.message,
    )
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


async def shift_conflict_handler(
    request: Request,
    exc: ShiftConflictError,
) -> JSONResponse:
    logger.info(
        "ShiftConflictError on %s %s: %s",
        request.method,
        request.url,
        exc.message,
    )
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s: %r", request.method, request.url, exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
