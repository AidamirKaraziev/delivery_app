from typing import Optional
from fastapi import Request


from selling_point.schemas import SellingPointGet
from selling_point_type.getters import getting_selling_point_type
from user.getters import getting_user


def getting_selling_point(obj: SellingPointGet, request: Optional[Request]) -> Optional[SellingPointGet]:
    if request is not None:
        url = request.url.hostname + ":8000" + "/static/"
        if obj.photo is not None:
            obj.photo = url + str(obj.photo)
        else:
            obj.photo = None
    return SellingPointGet(
        id=obj.id,
        name=obj.name,
        photo=obj.photo,
        selling_point_type_id=getting_selling_point_type(obj.type) if obj.type is not None else None,
        address=obj.address,
        client_id=getting_user(obj=obj.user, request=request) if obj.user is not None else None,
        is_active=obj.is_active
    )
