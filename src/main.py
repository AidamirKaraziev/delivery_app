from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from auth.base_config import auth_backend, fastapi_users
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate, UserUpdate, UserReadOld
from config import REDIS_HOST, REDIS_PORT

from role.router import router as router_role
from promo.router import router as router_promo
from dish.router import router as router_dish
from selling_point.router import router as router_selling_point
from selling_point_type.router import router as router_sp_type

from user.router import router as router_user, get_users_router
# from core.initial_data import create_initial_data
from cart.router import router as router_cart
from order.router import router as router_order
from our_status.router import router as router_status


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
    fastapi_users.get_register_router(UserReadOld, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_user)
app.include_router(
    get_users_router(user_schema=UserRead, user_update_schema=UserUpdate, get_user_manager=get_user_manager),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_role)
app.include_router(router_promo)
app.include_router(router_dish)
app.include_router(router_selling_point)
app.include_router(router_sp_type)
app.include_router(router_cart)
app.include_router(router_order)
app.include_router(router_status)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST:{REDIS_PORT}}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # await create_initial_data()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"
