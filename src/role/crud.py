from core.base_crud import CRUDBase
from role.models import Role
from role.schemas import RoleCreate, RoleUpdate


class CrudRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    pass


crud_role = CrudRole(Role)
