from typing import Optional
from selling_point_type.schemas import SellingPointTypeGet


def getting_selling_point_type(selling_point_type: SellingPointTypeGet) -> Optional[SellingPointTypeGet]:

    return SellingPointTypeGet(
        id=selling_point_type.id,
        name=selling_point_type.name,
        photo=selling_point_type.photo
    )
