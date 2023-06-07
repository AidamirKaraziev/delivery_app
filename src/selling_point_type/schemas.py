from typing import Optional
from pydantic import BaseModel


class SellingPointTypeGet(BaseModel):
    id: int
    name: str
    photo: str
    is_active: bool


class SellingPointTypeCreate(BaseModel):
    id: int
    name: str
    photo: str
    is_active: Optional[bool] = True


class SellingPointTypeUpdate(BaseModel):
    id: int
    name: str
    photo: str
    is_active: bool

