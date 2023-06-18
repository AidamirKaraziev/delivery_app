from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from status.models import Status
from status.schemas import StatusCreate, StatusUpdate

from core.base_crud import CRUDBase


class CrudStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):

    async def get_status_by_id(self, *, db: AsyncSession, status_id: int):
        status = await self.get(db=db, id=status_id)
        if status is None:
            return None, -2, None
        return status, 0, None

    async def get_all_statuses(self, *, db: AsyncSession, skip: int, limit: int):
        statuses = await self.get_multi(db_session=db, skip=skip, limit=limit)
        return statuses, 0, None

    async def create_status(self, *, db: AsyncSession, new_data: StatusCreate):
        # check by name
        query = select(self.model).where(self.model.name == new_data.name)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, -3, None
        new_status = await self.create(db_session=db, obj_in=new_data)
        return new_status, 0, None


crud_status = CrudStatus(Status)
