from pydantic import BaseModel


class OrderStatusGet(BaseModel):
    id: int
    name: str


class OrderStatusCreate(BaseModel):
    id: int
    name: str


class OrderStatusUpdate(BaseModel):
    name: str


