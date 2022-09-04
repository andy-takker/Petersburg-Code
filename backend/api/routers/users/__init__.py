from fastapi import APIRouter

from api.routers.users.career_test import career_test_router
from api.routers.users.user_events import user_event_router

router = APIRouter(prefix='/users')
router.include_router(router=user_event_router)
router.include_router(router=career_test_router)
