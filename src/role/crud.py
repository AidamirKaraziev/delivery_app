from typing import Optional

from core.base_crud import CRUDBase
from role.models import Role
from role.schemas import RoleCreate, RoleUpdate, RoleGet
from sqlalchemy.orm import Session


class CrudRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    pass


crud_role = CrudRole(Role)
