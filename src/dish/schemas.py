from typing import Optional
from pydantic import BaseModel, Field
from promo.schemas import PromoGet


class DishGet(BaseModel):
    id: Optional[int]
    name: Optional[str]

    main_photo: Optional[str]
    photo_1: Optional[str]
    photo_2: Optional[str]

    description: Optional[str]
    composition: Optional[str]
    price: Optional[int]

    promo_id: Optional[PromoGet]

    is_active: Optional[bool]

    visible: Optional[bool]


class DishCreate(BaseModel):

    name: str
    description: str

    composition: str
    price: int

    promo_id: Optional[int]
    is_active: Optional[bool] = True
    visible: Optional[bool] = False


class DishUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    composition: Optional[str]
    price: Optional[int]
    promo_id: Optional[int]
    is_active: Optional[bool]
    visible: Optional[bool]
