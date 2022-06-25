from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import get_settings
from database.engine import init_models
from api.routers import proektoria_router

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
    application.add_event_handler('startup', init_models)
    application.include_router(proektoria_router)
    return application


app = get_application()
