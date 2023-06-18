from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart.models import Cart
from cart.schemas import CartCreate, CartUpdate

from core.base_crud import CRUDBase


class CrudCart(CRUDBase[Cart, CartCreate, CartUpdate]):

    async def get_item_cart_by_id(self, *, db: AsyncSession, cart_id: int):
        obj = await self.get(db=db, id=cart_id)
        if obj is None:
            return None, -2, None
        return obj, 0, None

    async def get_cart_by_id(self, *, db: AsyncSession, cart_id: int):
        db_session = db or self.db.session
        query = select(self.model).where(self.model.cart_id == cart_id)
        response = await db_session.execute(query)
        objects = response.scalars().all()
        if objects is None:
            return None, -2, None
        return objects, 0, None

    async def get_all_carts(self, *, db: AsyncSession, skip: int, limit: int):
        objects = await self.get_multi(db_session=db, skip=skip, limit=limit)
        return objects, 0, None

    async def create_item_cart(self, *, db: AsyncSession, new_data: CartCreate):
        # check id
        query = select(self.model).where(self.model.id == new_data.item_id)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, -3, None
        objects = await self.create(db_session=db, obj_in=new_data)
        return objects, 0, None

    async def update_item_cart(self, *, db: AsyncSession, update_data: CartCreate, item_id: int):
        # check id
        query = select(self.model).where(self.model.id == item_id)
        response = await db.execute(query)
        current_obj = response.scalar_one_or_none()
        if current_obj is None:
            return None, -3, None
        objects = await self.update(db_session=db, obj_current=current_obj, obj_new=update_data)
        return objects, 0, None


crud_cart = CrudCart(Cart)
