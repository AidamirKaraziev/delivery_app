import time
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache

from core.response import SingleEntityResponse
from database import get_async_session
# from operations.getters import get_operation
from operations.getters import get_operation
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


@router.get("", response_model=SingleEntityResponse)
async def get_specific_operations(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        # print(result.first())
        d = result.first()
        if d is None:
            return SingleEntityResponse(data={})
        # return {
        #     "status": "success",
        #     "data": result.first(),
        #     "details": None
        # }
        return SingleEntityResponse(data=get_operation(d))
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    """
    docstring
    """
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}



@router.get("/my_test")
@cache(expire=30)
def get_my_test():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"

# # response_model=SingleEntityResponse
# @router.get("/get", response_model=ListOfEntityResponse)
# async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
#     try:
#         query = select(operation).where(operation.c.type == operation_type)
#         # print(query)
#         result = await session.execute(query)
#         print("1"*15, result.all())
#         # print(result.type)
#         # return ListOfEntityResponse(data=get_operation(operation=result.all()))
#         # return ListOfEntityResponse(data=[get_operation(operation=datum) for datum in result])
#         # return {
#         #     "status": "success",
#         #     "data": result.all(),
#         #     "details": None
#         # }
#         # print("1"*15, result.all())
#         # return result.all()
#         # print(result[1])
#     except Exception:
#         # Передать ошибку разработчикам
#         raise HTTPException(status_code=500, detail={
#             "status": "error",
#             "data": None,
#             "details": None
#         })























# import time
#
#
# from starlette.requests import Request
# from starlette.responses import Response
#
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
#
# from redis import asyncio as aioredis
#
# from fastapi import APIRouter, Depends, HTTPException, FastAPI
# from sqlalchemy import select, insert
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from database import get_async_session
# from operations.models import operation
# from operations.schemas import OperationCreate
#
# router = APIRouter(
#     prefix="/operations",
#     tags=["Operation"]
# )
#
#
# @router.get('/long_operation')
# @cache(expire=15)
# def get_long_op():
#     time.sleep(2)
#     return "Много-много данных, которые вычислялись сто лет"
#
#
# @router.get("/")
# async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
#     try:
#         query = select(operation).where(operation.c.type == operation_type)
#         result = await session.execute(query)
#         return {
#             "status": "success",
#             "data": [dict(r._mapping) for r in result],
#             "details": None
#         }
#     except Exception:
#         raise HTTPException(status_code=500, detail={
#             "status": "error",
#             "data": None,
#             "details": None
#         })
#
#
# @router.post("/")
# async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(operation).values(**new_operation.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}
