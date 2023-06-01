from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from operations.router import router as router_operation
from tasks.router import router as router_tasks

app = FastAPI(
    title="Trading App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(router_tasks)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# from auth.base_config import auth_backend, fastapi_users
# from auth.schemas import UserRead, UserCreate
# from fastapi_cache.decorator import cache
# from fastapi import FastAPI
# from starlette.requests import Request
# from starlette.responses import Response
#
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
#
#
# from redis import asyncio as aioredis
#
#
# from operations.router import router as router_operation
#
# app = FastAPI(
#     title="Trading App"
# )
#
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth",
#     tags=["Auth"],
# )
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Auth"],
# )
#
# app.include_router(router_operation)
#
#
# @cache()
# async def get_cache():
#     return 1
#
#
# @app.get("/test_my/")
# @cache(expire=60)
# async def index():
#     return dict(hello="world")
#
#
# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost", encodings="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#
#
#
#
# # from typing import Union
# #
# # from fastapi import Depends
# #
# # from fastapi import FastAPI
# # from fastapi_users import FastAPIUsers
# #
# # from auth.base_config import auth_backend
# # from auth.manager import get_user_manager
# # from auth.models import User
# # from auth.schemas import UserRead, UserCreate
# #
# # app = FastAPI(
# #     title="Treading App"
# # )
# #
# #
# # fastapi_users = FastAPIUsers[User, int](
# #     get_user_manager,
# #     [auth_backend],
# # )
# # app.include_router(
# #     fastapi_users.get_auth_router(auth_backend),
# #     prefix="/auth/jwt",
# #     tags=["auth"],
# # )
# #
# #
# # app.include_router(
# #     fastapi_users.get_register_router(UserRead, UserCreate),
# #     prefix="/auth",
# #     tags=["auth"],
# # )
# #
# # current_user = fastapi_users.current_user()
# #
# #
# # @app.get("/protected-route")
# # def protected_route(user: User = Depends(current_user)):
# #     return f"Hello, {user.username}"
# #
# #
# # @app.get("/unprotected-route")
# # def unprotected_route():
# #     return f"Hello, Мой милый друг!"
# #
# # # Код который можно использовать в будущем
# #
# #
# # async def common_parameters(
# #         q: Union[str, None] = None, skip: int = 0, limit: int = 100
# # ):
# #     return {"q": q, "skip": skip, "limit": limit}
# #
# #
# # @app.get("/items/")
# # async def read_items(
# #         commons: dict = Depends(common_parameters)
# # ):
# #     return commons
#
#
