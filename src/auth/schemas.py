from sqlite3 import Date
from typing import Optional

from fastapi_users import schemas

from role.schemas import RoleGet


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    photo: str

    email: str
    phone_number: str

    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    id: int
    name: str
    photo: str

    email: str
    phone_number: str

    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    id: int
    name: str
    photo: str

    email: str
    phone_number: str

    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserGet(schemas.BaseUser[int]):
    id: int
    name: str
    photo: str

    email: str
    phone_number: str
    registered_at: Optional[Date]

    role_id: Optional[RoleGet]
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True
