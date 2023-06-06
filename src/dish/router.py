from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.response import SingleEntityResponse, ListOfEntityResponse
from database import get_async_session
from dish.crud import crud_dish
from dish.getters import get_dish
from dish.models import Dish
from dish.schemas import DishGet

router = APIRouter(
    prefix="/dish",
    tags=["Dish"]
)


@router.get("/dish", response_model=SingleEntityResponse[DishGet])
async def get_dish(
        dish_id: int,
        session: AsyncSession = Depends(get_async_session)
):

    obj, code, indexes = crud_dish.get(db=session, id=dish_id)

    return SingleEntityResponse(data=get_dish(obj=obj))
