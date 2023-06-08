from typing import Optional

from auth.schemas import UserGet
from role.getters import getting_role


def getting_user(obj: UserGet) -> Optional[UserGet]:
    return UserGet(
        id=obj.id,
        name=obj.name,
        photo=obj.photo,
        email=obj.email,
        phone_number=obj.phone_number,
        registered_at=obj.registered_at,  # сделать вывод в юникс секундах
        role_id=getting_role(obj.role) if obj.role is not None else None,  # хз почему желтое не кайф
        is_active=obj.is_active,
        is_superuser=obj.is_superuser,
        is_verified=obj.is_verified,
    )