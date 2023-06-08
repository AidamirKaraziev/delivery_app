import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users
from auth.models import User
from core.response import ListOfEntityResponse
from database import get_async_session

from user.crud import crud_user
from user.getters import getting_user

current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get(
            path='/all/',
            response_model=ListOfEntityResponse,
            name='get_users',
            description='Получение списка всех рекламируемых групп'
            )
async def get_users(
        skip: int = 0,
        limit: int = 100,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    objects, code, indexes = await crud_user.get_all_users(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_user(obj) for obj in objects])


if __name__ == "__main__":
    logging.info('Running...')
