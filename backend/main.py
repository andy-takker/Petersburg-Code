from fastapi import FastAPI, HTTPException
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from config import get_settings
from database.engine import init_models
from api.routers import proektoria_router, user_router, event_router
from errors import http_exception_handler

settings = get_settings()


def get_application() -> FastAPI:
    """App Factory"""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        description='Код Петербурга',
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    application.add_exception_handler(
        exc_class_or_status_code=HTTPException,
        handler=http_exception_handler,
    )
    application.add_event_handler('startup', init_models)
    application.include_router(event_router)
    application.include_router(proektoria_router)
    application.include_router(user_router)
    add_pagination(application)
    return application


app = get_application()
