from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import UserCreate, UserUpdate
from core.base_crud import CRUDBase


class CrudUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_user_by_id(self, *, db: AsyncSession, user_id: int):
        obj = await super().get(db=db, id=user_id)
        if obj is None:
            return None, "Not found user with this id", None
        return obj, 0, None

    async def get_all_users(self, *, db: AsyncSession, skip: int, limit: int):
        objects = await super().get_multi(db_session=db, skip=skip, limit=limit)
        return objects, 0, None

    async def update_user(self, *, db: AsyncSession, update_data: UserUpdate, user_id: int):
        # check id
        query = select(self.model).where(self.model.id == user_id)
        resp = await db.execute(query)
        this_obj = resp.scalar_one_or_none()
        if this_obj is None:
            return None, "Not found user with this id", None  # not_found
        # check name
        query = select(self.model).where(self.model.email == update_data.email)
        response = await db.execute(query)
        if response.scalar_one_or_none() is not None:
            return None, "Email already exists", None
        # check change is_superuser
        if update_data.is_superuser is True:
            return None, "You will never change your rights.Stop it!", None
        # if update_data.is_active is not None

        objects = await super().update(db_session=db, obj_current=this_obj, obj_new=update_data)
        return objects, 0, None


crud_user = CrudUser(User)
