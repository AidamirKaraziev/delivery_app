import datetime
from typing import Optional

from fastapi_users import schemas
from datetime import datetime


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
    registered_atutcnow: datetime

    hashed_password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
