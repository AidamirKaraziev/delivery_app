from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dish.models import Dish
from dish.schemas import DishCreate, DishUpdate

from core.base_crud import CRUDBase


class CrudDish(CRUDBase[Dish, DishCreate, DishUpdate]):

    async def get_dish_by_id(self, *, db: AsyncSession, dish_id: int):
        obj = await self.get(db=db, id=dish_id)
        if obj is None:
            return None, "Not found dish with this id", None
        return obj, 0, None

    async def get_all_dishes(self, *, db: AsyncSession, skip: int, limit: int):
        objects = await self.get_multi(db_session=db, skip=skip, limit=limit)
        return objects, 0, None

    async def create_dish(self, *, db: AsyncSession, new_data: DishCreate):
        # check id
        query = select(self.model).where(self.model.name == new_data.name)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, "А dish with that name already exists", None
        objects = await self.create(db_session=db, obj_in=new_data)
        return objects, 0, None

    async def update_dish(self, *, db: AsyncSession, update_data: DishUpdate, dish_id: int):
        # check id
        query = select(self.model).where(self.model.id == dish_id)
        response = await db.execute(query)
        current_obj = response.scalar_one_or_none()
        if current_obj is None:
            return None, "Not found dish with this id", None
        # check name
        query = select(self.model).where(self.model.name == update_data.name)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, "А dish with that name already exists", None
        objects = await self.update(db_session=db, obj_current=current_obj, obj_new=update_data)
        return objects, 0, None


crud_dish = CrudDish(Dish)
