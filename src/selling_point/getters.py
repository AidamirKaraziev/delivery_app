from typing import Optional
from selling_point.schemas import SellingPointGet


def get_dish(obj: SellingPointGet) -> Optional[SellingPointGet]:

    return SellingPointGet(
        id=obj.id,
        name=obj.name,
        photo=obj.photo,
        sp_type_id=obj.sp_type_id,
        address=obj.address,
        client_id=obj.client_id,
    )
