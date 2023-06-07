import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users
from auth.models import User
from core.response import SingleEntityResponse, ListOfEntityResponse, Meta
from database import get_async_session

from user.crud import crud_user
from user.getters import getting_user

current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get(
            path="/me/",
            response_model=SingleEntityResponse,
            name='get_user_me',
            description='Вывод данных пользователя'
            )
async def get_user_me(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_user.get_user_by_id(db=session, user_id=user.id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail=code)
    return SingleEntityResponse(data=getting_user(obj=obj))


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


@router.get(
            path="/{user_id}",
            response_model=SingleEntityResponse,
            name='get_user',
            description='Вывод данных пользователя по идентификатору'
            )
async def get_user(
        user_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_user.get_user_by_id(db=session, user_id=user_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail=code)
    return SingleEntityResponse(data=getting_user(obj=obj))


# @router.put(path="/{me/}",
#             response_model=SingleEntityResponse,
#             name='update_user_me',
#             description='Изменить своих данных пользователем'
#             )
# async def update_user_me(
#         update_data: UserUpdate,
#         user: User = Depends(current_active_user),
#         session: AsyncSession = Depends(get_async_session),
# ):
#
#     obj, code, indexes = await crud_user.update_user(db=session,
#                                                        update_data=update_data,
#                                                        promo_id=promo_id)
#     # ошибки обработать
#     if code != 0:
#         return SingleEntityResponse(data=f"ERROR: {code}")
#     return SingleEntityResponse(data=getting_promo(obj=obj))


if __name__ == "__main__":
    logging.info('Running...')
