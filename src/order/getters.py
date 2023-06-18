from typing import Optional
from order.schemas import OrderGet


def getting_order(obj: OrderGet) -> Optional[OrderGet]:

    selling_point_data = None
    if obj.selling_point:
        selling_point_data = {
            "id": obj.selling_point.id,
            "name": obj.selling_point.name,
            "photo": obj.selling_point.photo,
            "selling_point_type_id": obj.selling_point.selling_point_type_id,
            "address": obj.selling_point.address,
            "client_id": obj.selling_point.client_id,
            "is_active": obj.selling_point.is_active
        }

    cart_data = None
    if obj.cart:
        cart_data = {
            "cart_id": obj.cart.cart_id,
            "dish_id": obj.cart.dish_id,
            "amount": obj.cart.amount,
            "sum": obj.cart.sum,
            "dish": obj.cart.dish
        }

    status_data = None
    if obj.status:
        status_data = {
            "id": obj.status.id,
            "name": obj.status.name
        }

    return OrderGet(
        id=obj.id,
        selling_point_id=selling_point_data,
        cart_id=cart_data,

        amount=obj.amount,
        sum=obj.sum,

        created_at=obj.created_at,
        completed_at=obj.completed_at,

        status_id=status_data,
        is_active=obj.is_active
    )
