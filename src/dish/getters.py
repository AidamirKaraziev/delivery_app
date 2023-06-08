from typing import Optional
from dish.schemas import DishGet
from promo.schemas import PromoGet


def getting_dish(obj: DishGet) -> Optional[DishGet]:

    promo_data = None
    if obj.promo:
        promo_data = {
            "id": obj.promo.id,
            "name": obj.promo.name
        }

    return DishGet(
        id=obj.id,
        name=obj.name,

        main_photo=obj.main_photo,
        photo1=obj.photo1,
        photo2=obj.photo2,

        discription=obj.discription,
        composition=obj.composition,
        price=obj.price,

        promo_id=promo_data,
        is_active=obj.is_active,
        visible=obj.visible,
    )
