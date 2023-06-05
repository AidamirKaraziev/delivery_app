from typing import Optional

from advertising_gr.schemas import AdvertisingGrGet


def getting_ad_gr(obj: AdvertisingGrGet) -> Optional[AdvertisingGrGet]:
    return AdvertisingGrGet(
        id=obj.id,
        name=obj.name,
    )
