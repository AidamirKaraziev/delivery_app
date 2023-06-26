from typing import Optional
from order.schemas import OrderGet
from cart.getters import getting_cart
from selling_point.getters import getting_selling_point
from our_status.getters import getting_status


def getting_order(obj: OrderGet) -> Optional[OrderGet]:

    return OrderGet(
        id=obj.id,
        selling_point_id=getting_selling_point(obj.selling_point_id) if obj.selling_point_id is not None else None,
        cart_id=getting_cart(obj.cart_id) if obj.cart_id is not None else None,

        amount=obj.amount,
        sum=obj.sum,

        created_at=obj.created_at,
        completed_at=obj.completed_at,

        status_id=getting_status(obj.status_id) if obj.status_id is not None else None,
        is_active=obj.is_active
    )
