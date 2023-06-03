from core.base_crud import CRUDBase
from dish.models import Dish
from dish.schemas import DishCreate, DishUpdate


class CrudDish(CRUDBase[Dish, DishCreate, DishUpdate]):
    pass


crud_dish = CrudDish(Dish)
