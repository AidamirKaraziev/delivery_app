from typing import Optional
from pydantic import BaseModel

from dish.schemas import DishGet


class CartGet(BaseModel):
    item_id: int
    cart_id: int
    dish_id: Optional[DishGet] = None
    amount: int
    sum: float


class CartCreate(BaseModel):
    item_id: int
    cart_id: int
    dish_id: int
    amount: int
    sum: float


class CartUpdate(BaseModel):
    item_id: int
    cart_id: int
    dish_id: int
    amount: int
    sum: float





