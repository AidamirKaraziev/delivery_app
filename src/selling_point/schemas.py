from typing import Optional
from pydantic import BaseModel
from auth.schemas import UserRead
from selling_point_type.schemas import SellingPointTypeGet


class SellingPointGet(BaseModel):
    id: int
    name: str
    photo: str
    selling_point_type_id: Optional[SellingPointTypeGet] = None
    address: str
    client_id: Optional[UserRead]
    is_active: bool


class SellingPointCreate(BaseModel):
    name: str
    photo: str
    selling_point_type_id: Optional[int] = None
    address: str
    client_id: int
    is_active: Optional[bool] = True


class SellingPointUpdate(BaseModel):
    name: str
    photo: str
    selling_point_type_id: Optional[int] = None
    address: str
    client_id: int
    is_active: bool
