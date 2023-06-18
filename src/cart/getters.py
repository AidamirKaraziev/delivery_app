from typing import Optional

from cart.schemas import CartGet


def getting_cart(obj: CartGet) -> Optional[CartGet]:

    dish_data = None
    if obj.dish:
        dish_data = {
            "id": obj.dish.id,
            "name": obj.dish.name,

            "main_photo": obj.dish.main_photo,
            "photo1": obj.dish.photo1,
            "photo2": obj.dish.photo2,

            "discription": obj.dish.discription,
            "composition": obj.dish.composition,
            "price": obj.dish.price,

            "promo_id": obj.dish.promo_id,
            "is_active": obj.dish.is_active,
            "visible": obj.dish.visible
        }

    return CartGet(
        item_id=obj.id,
        cart_id=obj.cart_id,
        dish_id=dish_data,
        amount=obj.amount,
        sum=obj.sum,
    )
