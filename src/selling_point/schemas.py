from typing import Optional
from pydantic import BaseModel
from auth.schemas import UserRead
from selling_point_type.schemas import SellingPointTypeGet


class SellingPointGet(BaseModel):
    id: int
    name: str
    photo: str
    type: Optional[SellingPointTypeGet] = None
    address: str
    client_id: Optional[UserRead]


class SellingPointCreate(BaseModel):
    id: int
    name: str
    photo: str
    type: Optional[int] = None
    address: str
    client_id: int


class SellingPointUpdate(BaseModel):
    id: int
    name: str
    photo: str
    type: Optional[int] = None
    address: str
    client_id: int

