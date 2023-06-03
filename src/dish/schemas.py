from pydantic import BaseModel, Field
from advertising_gr.getters import AdvertisingGrGet


class DishGet(BaseModel):
    id: int
    name: str

    main_photo: str
    photo1: str
    photo2: str

    discription: str
    composition: str
    price: float

    advertising_gr_id: int
    visible: bool


class DishCreate(BaseModel):
    id: int
    name: str

    main_photo: str
    photo1: str
    photo2: str

    discription: str
    composition: str
    price: float

    advertising_gr_id: AdvertisingGrGet


class DishUpdate(BaseModel):
    name: str = Field(..., title='Наименование блюда')

    main_photo: str
    photo1: str
    photo2: str

    discription: str
    composition: str
    price: float

    advertising_gr_id: int

