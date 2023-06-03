from typing import Optional
from dish.schemas import DishGet


def get_dish(obj: DishGet) -> Optional[DishGet]:

    return DishGet(
        id=obj.id,
        name=obj.name,

        main_photo=obj.main_photo,
        photo1=obj.photo1,
        photo2=obj.photo2,

        discription=obj.discription,
        composition=obj.composition,
        price=obj.price,

        advertising_gr_id=obj.advertising_gr_id,
        visible=obj.visible,
    )
