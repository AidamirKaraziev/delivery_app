from pydantic import BaseModel


class SellingPointTypeGet(BaseModel):
    id: int
    name: str
    photo: str


class SellingPointTypeCreate(BaseModel):
    id: int
    name: str
    photo: str


class SellingPointTypeUpdate(BaseModel):
    id: int
    name: str
    photo: str

