from pydantic import BaseModel


class SellingPointGet(BaseModel):
    id: int
    name: str
    svg: str


class SellingPointCreate(BaseModel):
    id: int
    name: str
    svg: str


class SellingPointUpdate(BaseModel):
    id: int
    name: str
    svg: str

