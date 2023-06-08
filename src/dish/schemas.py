from typing import Optional, Union
from pydantic import BaseModel, Field
from promo.schemas import PromoGet


class DishGet(BaseModel):

    id: int
    name: str

    main_photo: str
    photo1: str
    photo2: str

    discription: str
    composition: str
    price: float

    promo_id: Optional[PromoGet] = None
    is_active: bool
    visible: Optional[bool] = True


class DishCreate(BaseModel):
    id: int
    name: str

    main_photo: str
    photo1: str
    photo2: str

    discription: str
    composition: str
    price: float

    promo_id: Optional[int] = None
    is_active: Optional[bool] = True
    visible: Optional[bool] = True


class DishUpdate(BaseModel):
    name: str = Field(..., title='Наименование блюда')

    main_photo: str
    photo1: str
    photo2: str

    discription: str
    composition: str
    price: float

    promo_id: Optional[int] = None
    is_active: bool
    visible: Optional[bool] = True

