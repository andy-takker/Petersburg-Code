from fastapi import HTTPException
from loguru import logger
from pydantic import BaseModel
from starlette.responses import JSONResponse

class ErrorResult(BaseModel):
    code: int
    message: str


def http_exception_handler(request, exc: HTTPException):
    """Хэндлер для HTTPException"""
    logger.warning(f'Exception with status code: {exc.status_code}')
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResult(code=exc.status_code, message=exc.detail).dict(),
    )