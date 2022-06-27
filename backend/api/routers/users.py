from typing import Optional

from fastapi import APIRouter

router = APIRouter(prefix='/users')


@router.get("/{user_id}/events")
async def get_user_events(
    user_id: int,
    is_favorite: Optional[bool] = None,
    is_involved: Optional[bool] = None,
):

    return

@router.post("/{user_id}/events")
async def update_user_events(
        user_id: int,
):
    return