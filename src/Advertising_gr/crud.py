from Advertising_gr.models import AdvertisingGr
from Advertising_gr.schemas import AdvertisingGrCreate, AdvertisingGrUpdate
from core.base_crud import CRUDBase


class CrudAdvertisingGr(CRUDBase[AdvertisingGr, AdvertisingGrCreate, AdvertisingGrUpdate]):

    pass


crud_advertising_gr = CrudAdvertisingGr(AdvertisingGr)
