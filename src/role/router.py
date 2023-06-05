# import time
# import json
#
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import select, insert
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from fastapi_cache.decorator import cache
#
# from core.response import SingleEntityResponse, ListOfEntityResponse
# from database import get_async_session
# from role.crud import crud_role
# from role.getters import get_role
# from role.models import Role
# from role.schemas import RoleGet
#
# router = APIRouter(
#     prefix="/role",
#     tags=["Role"]
# )

#
# @router.get("/roles",
#             response_model=ListOfEntityResponse[RoleGet])
# async def get_roles():
#     return
#
#
# @router.get("/role",
#             response_model=SingleEntityResponse[RoleGet])
# async def get_roles(
#         role_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#
#     obj, code, indexes = crud_role.get(db=session, id=role_id)
#     # Вывод ошибки с подробным описанием(Личная разработка Айдамира Каразиева(пиздатого парня))
#     # get_raise(code=code)
#
#     return SingleEntityResponse(data=get_role(obj=obj))


import logging
import time
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert

from core.exception import UnfoundEntity
from core.response import SingleEntityResponse, ListOfEntityResponse, Meta
from role import crud
from role.crud import crud_role
from role.getters import getting_role

from role.schemas import RoleGet
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from role.models import Role

router = APIRouter(
    prefix="/role",
    tags=["Role"]
)


#  код реализованный через offset - limit
# Вывод всех Должностей
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
            # response_model=SingleEntityResponse[RoleGet]
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

#
# @router.get("/",
#             response_model=SingleEntityResponse)
# async def get_role(
#         role_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     query = select(Role).where(Role.id == role_id)
#     result = await session.execute(query)
#     role = result.scalar_one_or_none()
#     return SingleEntityResponse(data=getting_role(obj=role))
    # дописать вывод ошибки, вернуть RoleGet в response_model
    # Надо продумать как выводить ошибки с ними ошибочка))))
    # if code == -1:
    #     raise UnfoundEntity(
    #         message=f"Ошибка мать его ты куда смотрел уебан!!",
    #         num=code,
    #         description=f"Ошибка мать его ты куда смотрел уебан!!",
    #         path="$.body"
    #     )
    # Вывод ошибки с подробным описанием(Личная разработка Айдамира Каразиева(пиздатого парня))
    # get_raise(code=code)


if __name__ == "__main__":
    logging.info('Running...')
