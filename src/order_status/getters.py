from typing import Optional
from order_status.schemas import OrderStatusGet


def getting_status(obj: OrderStatusGet) -> Optional[OrderStatusGet]:

    return OrderStatusGet(
        id=obj.id,
        name=obj.name
    )
