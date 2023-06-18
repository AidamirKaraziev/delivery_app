import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users
from auth.models import User
from core.response import SingleEntityResponse, ListOfEntityResponse
from database import get_async_session
from cart.crud import crud_cart
from cart.getters import getting_cart
from cart.schemas import CartCreate, CartUpdate

current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get(
    path="/{item_id}",
    response_model=ListOfEntityResponse,
    name='get_item_cart_by_id',
    description='Вывод корзины по идентификатору'
)
async def get_item_cart_by_id(
        item_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    item, code, indexes = await crud_cart.get_item_cart_by_id(db=session, cart_id=item_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return SingleEntityResponse(data=get_item_cart_by_id(obj=item))


@router.get(
    path="/{cart_id}",
    response_model=ListOfEntityResponse,
    name='get_cart_by_cart_id',
    description='Вывод корзины по идентификатору'
)
async def get_cart_by_cart_id(
        cart_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    cart_items, code, indexes = await crud_cart.get_cart_by_id(db=session, cart_id=cart_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return ListOfEntityResponse(data=[getting_cart(item) for item in cart_items])


@router.post(
    path="/",
    response_model=SingleEntityResponse,
    name='create_cart_item',
    description='Добавление позиции в корзину'
)
async def create_cart_item(
        new_data: CartCreate,
        user: User = Depends(current_active_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_cart.create_item_cart(db=session, new_data=new_data)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=409, detail="Resource already exists")
    return SingleEntityResponse(data=get_item_cart_by_id(obj=obj))


@router.put(
    path="/{item_id}",
    response_model=SingleEntityResponse,
    name='update_cart_item',
    description='Изменение позиции в корзине'
)
async def update_cart_item(
        update_data: CartUpdate,
        item_id: int,
        user: User = Depends(current_active_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    item_cart, code, indexes = await crud_cart.update_item_cart(db=session,
                                                                update_data=update_data,
                                                                item_id=item_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return SingleEntityResponse(data=get_item_cart_by_id(obj=item_cart))


if __name__ == "__main__":
    logging.info('Running...')
