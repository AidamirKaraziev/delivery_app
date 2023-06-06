from typing import Optional
from pydantic import BaseModel, Field


class PromoGet(BaseModel):
    id: int
    name: str


# формальность
class PromoCreate(BaseModel):
    name: str = Field(..., title="Должность")


# формальность
class PromoUpdate(BaseModel):
    name: str = Field(..., title="Должность")


