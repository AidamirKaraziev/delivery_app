from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from order.models import Order
from order.schemas import OrderCreate, OrderUpdate

from core.base_crud import CRUDBase


class CrudOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    async def get_order_by_id(self, *, db: AsyncSession, order_id: int):
        obj = await self.get(db=db, id=order_id)
        if obj is None:
            return None, -2, None
        return obj, 0, None

    async def get_all_orders(self, *, db: AsyncSession, skip: int, limit: int):
        objects = await self.get_multi(db_session=db, skip=skip, limit=limit)
        return objects, 0, None

    async def create_order(self, *, db: AsyncSession, new_data: OrderCreate):
        # check cart_id
        query = select(self.model).where(self.model.cart_id == new_data.cart_id)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, -3, None
        objects = await self.create(db_session=db, obj_in=new_data)
        return objects, 0, None

    async def update_order(self, *, db: AsyncSession, update_data: OrderUpdate, order_id: int):
        # check id
        query = select(self.model).where(self.model.id == order_id)
        response = await db.execute(query)
        current_obj = response.scalar_one_or_none()
        if current_obj is None:
            return None, -3, None
        objects = await self.update(db_session=db, obj_current=current_obj, obj_new=update_data)
        return objects, 0, None


crud_order = CrudOrder(Order)
