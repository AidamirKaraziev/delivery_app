from pydantic import BaseModel


class SellingPointGet(BaseModel):
    id: int
    name: str
    photo: str
    sp_type_id: int
    address: str
    client_id: int


class SellingPointCreate(BaseModel):
    id: int
    name: str
    photo: str
    sp_type_id: int
    address: str
    client_id: int


class SellingPointUpdate(BaseModel):
    id: int
    name: str
    photo: str
    sp_type_id: int
    address: str
    client_id: int

