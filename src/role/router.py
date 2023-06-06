import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from role.crud import crud_role
from role.getters import getting_role

from core.response import SingleEntityResponse, ListOfEntityResponse, Meta
from database import get_async_session


router = APIRouter(
    prefix="/role",
    tags=["Role"]
)


@router.get('/all',
            response_model=ListOfEntityResponse,
            name='Список ролей',
            description='Получение списка всех ролей'
            )
async def get_roles(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session),
):
    objects, code, indexes = await crud_role.get_all_role(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_role(obj) for obj in objects])


@router.get("/",
            response_model=SingleEntityResponse
            )
async def get_role(
        role_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_role.get_role_by_id(db=session, role_id=role_id)
    # ошибки обработать
    if code == -1:
        return SingleEntityResponse(data="ERROR")
    return SingleEntityResponse(data=getting_role(obj=obj))


if __name__ == "__main__":
    logging.info('Running...')
