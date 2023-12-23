from sqlalchemy.ext.asyncio import AsyncSession

from order_status.models import OrderStatus
from order_status.schemas import OrderStatusCreate, OrderStatusUpdate

from core.base_crud import CRUDBase


class CrudOrderStatus(CRUDBase[OrderStatus, OrderStatusCreate, OrderStatusUpdate]):

    async def get_status_by_id(self, *, db: AsyncSession, status_id: int):
        obj = await self.get(db=db, id=status_id)
        if obj is None:
            return None, "Not found order_status with this id", None
        return obj, 0, None

    async def get_all_statuses(self, *, db: AsyncSession, skip: int, limit: int):
        objects = await self.get_multi(db_session=db, skip=skip, limit=limit)
        return objects, 0, None


crud_status = CrudOrderStatus(OrderStatus)
