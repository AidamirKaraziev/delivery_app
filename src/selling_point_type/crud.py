from core.base_crud import CRUDBase
from selling_point.models import SellingPoint
from selling_point.schemas import SellingPointCreate, SellingPointUpdate


class CrudSellingPoint(CRUDBase[SellingPoint, SellingPointCreate, SellingPointUpdate]):
    pass


crud_selling_point = CrudSellingPoint(SellingPoint)
