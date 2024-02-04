from fastapi import Request
from typing import Optional
from dish.schemas import DishGet
from promo.getters import getting_promo

from config import APP_PORT


def getting_dish(obj: DishGet, request: Request) -> Optional[DishGet]:
    if request is not None:
        url = request.url.hostname + f":{APP_PORT}" + "/static/"
        if obj.main_photo is not None:
            obj.main_photo = url + str(obj.main_photo)
        else:
            obj.main_photo = None
        if obj.photo_1 is not None:
            obj.photo_1 = url + str(obj.photo_1)
        else:
            obj.photo_1 = None
        if obj.photo_2 is not None:
            obj.photo_2 = url + str(obj.photo_2)
        else:
            obj.photo_2 = None

    return DishGet(
        id=obj.id,
        name=obj.name,
        main_photo=obj.main_photo,
        photo_1=obj.photo_1,
        photo_2=obj.photo_2,

        description=obj.description,
        composition=obj.composition,
        price=obj.price,

        promo_id=getting_promo(obj.promo) if obj.promo is not None else None,
        is_active=obj.is_active,
        visible=obj.visible,
    )
