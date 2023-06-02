from typing import Optional

from Advertising_gr.schemas import AdvertisingGrGet


def get_advertising_gr(obj: AdvertisingGrGet) -> Optional[AdvertisingGrGet]:
    return AdvertisingGrGet(
        id=obj.id,
        name=obj.name,
    )
