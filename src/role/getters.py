from typing import Optional
from fastapi import Request
from role.schemas import RoleGet


def getting_role(obj: RoleGet) -> Optional[RoleGet]:

    return RoleGet(
        id=obj.id,
        name=obj.name,
        permissions=obj.permissions,
    )
