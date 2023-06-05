from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from advertising_gr.models import AdvertisingGr
from advertising_gr.schemas import AdvertisingGrCreate, AdvertisingGrUpdate

from core.base_crud import CRUDBase


class CrudAdvertisingGr(CRUDBase[AdvertisingGr, AdvertisingGrCreate, AdvertisingGrUpdate]):

    async def get_ad_gr_by_id(self, *, db: AsyncSession, ad_gr_id: int):
        obj = await super().get(db=db, id=ad_gr_id)
        if obj is None:
            return None, -2, None
        return obj, 0, None

    async def get_all_ad_gr(self, *, db: AsyncSession, skip: int, limit: int):
        objects = await super().get_multi(db_session=db, skip=skip, limit=limit)
        return objects, 0, None

    async def create_ad_gr(self, *, db: AsyncSession, new_data: AdvertisingGrCreate):
        # check name
        query = select(self.model).where(self.model.name == new_data.name)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, -3, None
        objects = await super().create(db_session=db, obj_in=new_data)
        return objects, 0, None

    async def update_ad_gr(self, *, db: AsyncSession, update_data: AdvertisingGrCreate, ad_gr_id: int):
        # check id
        query = select(self.model).where(self.model.id == ad_gr_id)
        resp = await db.execute(query)
        this_obj = resp.scalar_one_or_none()
        if this_obj is None:
            return None, -4, None  # not_found
        # check name
        query = select(self.model).where(self.model.name == update_data.name)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, -3, None
        objects = await super().update(db_session=db, obj_current=this_obj, obj_new=update_data)
        return objects, 0, None


crud_ad_gr = CrudAdvertisingGr(AdvertisingGr)
