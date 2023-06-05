from typing import Optional

from core.base_crud import CRUDBase
from role.models import Role
from role.schemas import RoleCreate, RoleUpdate, RoleGet
from sqlalchemy.orm import Session


class CrudRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    async def get_role_by_id(self):

        return


crud_role = CrudRole(Role)
