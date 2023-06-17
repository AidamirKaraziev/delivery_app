from typing import Optional
from pydantic import BaseModel
from auth.schemas import UserGet
from selling_point_type.schemas import SellingPointTypeGet


class SellingPointGet(BaseModel):
    id: int
    name: str
    photo: Optional[str]
    selling_point_type_id: Optional[SellingPointTypeGet]
    address: str
    client_id: Optional[UserGet]
    is_active: Optional[bool]


class SellingPointCreate(BaseModel):
    name: str
    selling_point_type_id: Optional[int]
    address: str
    client_id: Optional[int]
    is_active: Optional[bool] = True


class SellingPointUpdate(BaseModel):
    name: Optional[str]
    selling_point_type_id: Optional[int]
    address: Optional[str]
    is_active: Optional[bool]
