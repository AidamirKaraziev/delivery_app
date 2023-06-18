import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users
from auth.models import User
from status.crud import crud_status
from status.getters import getting_status

from core.response import SingleEntityResponse, ListOfEntityResponse, Meta
from database import get_async_session

current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(
    prefix="/status",
    tags=["Status"]
)


@router.get(
            path="/all",
            response_model=ListOfEntityResponse,
            name='get_statuses',
            description='Получение списка всех статусов'
            )
async def get_statuses(
        skip: int = 0,
        limit: int = 100,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    objects, code, indexes = await crud_status.get_all_statuses(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_status(obj) for obj in objects])


@router.get(
            path="/{status_id}",
            response_model=SingleEntityResponse,
            name="get_status",
            description='Вывод статуса по идентификатору'
            )
async def get_status(
        status_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_status.get_status_by_id(db=session, status_id=status_id)
    # ошибки обработать
    if code == -1:
        return SingleEntityResponse(data="ERROR")
    return SingleEntityResponse(data=getting_status(obj=obj))


if __name__ == "__main__":
    logging.info('Running...')
