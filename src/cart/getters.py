from typing import Optional
from cart.schemas import CartGet
from dish.getters import getting_dish


def getting_cart(obj: CartGet) -> Optional[CartGet]:

    return CartGet(
        item_id=obj.id,
        cart_id=obj.cart_id,
        dish_id=getting_dish(obj.dish) if obj.dish is not None else None,
        amount=obj.amount,
        sum=obj.sum,
    )
