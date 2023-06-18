from typing import Optional
from pydantic import BaseModel


class SellingPointTypeGet(BaseModel):
    id: Optional[int]
    name: Optional[str]
    photo: Optional[str]
    is_active: bool


class SellingPointTypeCreate(BaseModel):
    name: str
    photo: str
    is_active: Optional[bool] = True


class SellingPointTypeUpdate(BaseModel):
    id: int
    name: str
    photo: str
    is_active: bool

