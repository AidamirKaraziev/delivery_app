import time
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache

from core.response import SingleEntityResponse, ListOfEntityResponse
from database import get_async_session
from role.crud import crud_role
from role.getters import get_role
from role.models import Role
from role.schemas import RoleGet

router = APIRouter(
    prefix="/role",
    tags=["Role"]
)

#
# @router.get("/roles",
#             response_model=ListOfEntityResponse[RoleGet])
# async def get_roles():
#     return


@router.get("/role",
            response_model=SingleEntityResponse[RoleGet])
async def get_roles(
        role_id: int,
        session: AsyncSession = Depends(get_async_session),
):

    obj, code, indexes = crud_role.get(db=session, id=role_id)
    # Вывод ошибки с подробным описанием(Личная разработка Айдамира Каразиева(пиздатого парня))
    # get_raise(code=code)

    return SingleEntityResponse(data=get_role(obj=obj))
