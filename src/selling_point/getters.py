from typing import Optional
from selling_point.schemas import SellingPointGet
from auth.schemas import UserRead
from selling_point_type.schemas import SellingPointTypeGet


def getting_selling_point(selling_point: SellingPointGet) -> Optional[SellingPointGet]:

    user_data = None
    if selling_point.user:
        user_data = {
            'id': selling_point.user.id,
            'name': selling_point.user.name,
            'photo': selling_point.user.photo,
            'email': selling_point.user.email,
            'phone_number': selling_point.user.phone_number,
            'role_id': selling_point.user.role_id,
            'is_active': selling_point.user.is_active,
            'is_superuser': selling_point.user.is_superuser,
            'is_verified': selling_point.user.is_verified
        }

    selling_point_type_data = None
    if selling_point.type:
        selling_point_type_data = {
            'id': selling_point.type.id,
            'name': selling_point.type.name
        }

    return SellingPointGet(
        id=selling_point.id,
        name=selling_point.name,
        photo=selling_point.photo,
        selling_point_type_id=selling_point_type_data,
        address=selling_point.address,
        client_id=user_data,
    )
