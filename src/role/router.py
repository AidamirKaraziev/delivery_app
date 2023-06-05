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


@router.get("/test")
async def get_test(
        role_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Role).where(Role.id == role_id)
        result = await session.execute(query)
        sexy = result.scalars().all()
        # d = result.all()
        print("SEXY=", sexy)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
# #  код реализованный через offset - limit
# # Вывод всех Должностей
# @router.get('/all',
#             response_model=ListOfEntityResponse,
#             name='Список Должностей',
#             description='Получение списка всех Должностей'
#             )
# async def get_roles(
#         skip: int = 0,
#         limit: int = 100,
#         session=Depends(get_session),
# ):
#     # logging.info(crud_role.get_multi(db=session, page=None))
#     # data = crud_role.get_multi(db=session, skip=skip, limit=limit)
#     # query = select(Role).where(Role.c.type == ro
#     pass
#
#     # return ListOfEntityResponse(data=[getting_role(datum) for datum in data])


# @router.get("/",
#             response_model=SingleEntityResponse[RoleGet])
# async def get_role(
#         role_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     test = crud_role.get(db=session, id=role_id)
#     return SingleEntityResponse(data=getting_role(obj=test))


@router.get("/"
            # response_model=SingleEntityResponse[RoleGet]
)
async def get_role(
        role_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    query = select(Role).where(Role.id == role_id)
    result = await session.execute(query)
    d = result.first()
    print(d)

    return d
    # d = result.all()
    # print(type(d))
    # return result.all()
    # # Сериализация результата в JSON
    # serialized_result = json.dumps([row for row in d])
    # print(serialized_result)
    # print(result.first())

    # return SingleEntityResponse(data=d)
    # return SingleEntityResponse(data=getting_role(obj=result.first()))
    # print(("123"*10, f"{test}")*12)
    # query = select(Role).where(Role.id == role_id)
    # result = await session.execute(query)
    # return result.all()
    # obj, code, indexes = crud_role.get_role_by_id(db=session, role_id=role_id)

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
