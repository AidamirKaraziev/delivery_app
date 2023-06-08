import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users
from auth.models import User
from core.response import SingleEntityResponse, ListOfEntityResponse
from database import get_async_session
from dish.crud import crud_dish
from dish.getters import getting_dish
from dish.schemas import DishCreate, DishUpdate

current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(
    prefix="/dish",
    tags=["Dish"]
)


@router.get(
    path='/dishes',
    response_model=ListOfEntityResponse,
    name='get_dishes',
    description='Получение списка всех блюд'
)
async def get_dishes(
        limit: int = 100,
        skip: int = 0,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    dishes, code, indexes = await crud_dish.get_all_dishes(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_dish(dish) for dish in dishes])


@router.get(
    path="/{dish_id}",
    response_model=SingleEntityResponse,
    name='get_dish_by_id',
    description='Вывод блюда по идентификатору'
)
async def get_dish_by_id(
        dish_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    dish, code, indexes = await crud_dish.get_dish_by_id(db=session, dish_id=dish_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return SingleEntityResponse(data=getting_dish(obj=dish))


@router.post(
    path="/",
    response_model=SingleEntityResponse,
    name='create_dish',
    description='Добавление блюда'
)
async def create_dish(
        new_data: DishCreate,
        user: User = Depends(current_active_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_dish.create_dish(db=session, new_data=new_data)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=409, detail="Resource already exists")
    return SingleEntityResponse(data=getting_dish(obj=obj))


@router.put(
    path="/{dish_id}",
    response_model=SingleEntityResponse,
    name='update_dish',
    description='Изменение блюда'
)
async def update_dish(
        update_data: DishUpdate,
        dish_id: int,
        user: User = Depends(current_active_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    dish, code, indexes = await crud_dish.update_dish(db=session,
                                                      update_data=update_data,
                                                      dish_id=dish_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return SingleEntityResponse(data=getting_dish(obj=dish))


if __name__ == "__main__":
    logging.info('Running...')
