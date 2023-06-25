from typing import Optional
from pydantic import BaseModel

from dish.schemas import DishGet


class CartGet(BaseModel):
    id: int
    order_id: int
    dish_id: Optional[DishGet] = None
    amount: int
    sum: float


class CartCreate(BaseModel):
    order_id: int
    dish_id: int
    amount: int
    sum: float


class CartUpdate(BaseModel):
    order_id: int
    dish_id: int
    amount: int
    sum: float





