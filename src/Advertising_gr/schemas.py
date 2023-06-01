from typing import Optional
from pydantic import BaseModel, Field


class AdvertisingGrGet(BaseModel):
    id: int
    name: str


# формальность
class AdvertisingGrCreate(BaseModel):
    name: str = Field(..., title="Должность")


# формальность
class AdvertisingGrUpdate(BaseModel):
    name: str = Field(..., title="Должность")


