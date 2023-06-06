from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from auth.base_config import auth_backend, fastapi_users
from auth.models import User
from auth.schemas import UserRead, UserCreate

from role.router import router as router_role
from promo.router import router as router_promo

current_user = fastapi_users.current_user()

app = FastAPI(
    title="Delivery App"
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

app.include_router(router_role)
app.include_router(router_promo)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"
