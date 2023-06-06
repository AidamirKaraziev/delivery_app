from core.base_crud import CRUDBase
from dish.models import Dish
from dish.schemas import DishCreate, DishUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class CrudDish(CRUDBase[Dish, DishCreate, DishUpdate]):
    async def get_dish_by_id(self, *, db: AsyncSession, dish_id: int):
        obj = await super().get(db=db, id=dish_id)
        if obj is None:
            return None, -1, None
        return obj, 0, None

    async def get_all_dishes(self, *, db: AsyncSession, skip: int, limit: int):
        obj = await super().get_multi(db_session=db, skip=skip, limit=limit)
        return obj, 0, None


crud_dish = CrudDish(Dish)
