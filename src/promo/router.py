import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.response import SingleEntityResponse, ListOfEntityResponse, Meta
from database import get_async_session
from promo.crud import crud_promo
from promo.getters import getting_promo
from promo.schemas import PromoUpdate, PromoCreate

router = APIRouter(
    prefix="/promo",
    tags=["Promo"]
)


@router.get('/all',
            response_model=ListOfEntityResponse,
            name='Список рекламируемых групп',
            description='Получение списка всех рекламируемых групп'
            )
async def get_promo(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session),
):
    objects, code, indexes = await crud_promo.get_all_promo(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_promo(obj) for obj in objects])


@router.get("/",
            response_model=SingleEntityResponse,
            name='Вывод рекламируемой группы по айди',
            description='Вывод рекламируемой группы по айди'
            )
async def get_promo(
        promo_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_promo.get_promo_by_id(db=session, promo_id=promo_id)
    # ошибки обработать
    if code != 0:
        return SingleEntityResponse(data=f"ERROR: {code}")
    return SingleEntityResponse(data=getting_promo(obj=obj))


@router.post("/",
             response_model=SingleEntityResponse,
             name='Создать рекламируемую группу',
             description='Создать рекламируемую группу'
             )
async def create_promo(
        new_data: PromoCreate,
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_promo.create_promo(db=session, new_data=new_data)
    # ошибки обработать
    if code != 0:
        return SingleEntityResponse(data=f"ERROR: {code}")
    return SingleEntityResponse(data=getting_promo(obj=obj))


@router.put("/",
            response_model=SingleEntityResponse,
            name='Изменить рекламируемую группу',
            description='Изменить рекламируемую группу'
            )
async def update_promo(
        update_data: PromoUpdate,
        promo_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_promo.update_promo(db=session,
                                                       update_data=update_data,
                                                       promo_id=promo_id)
    # ошибки обработать
    if code != 0:
        return SingleEntityResponse(data=f"ERROR: {code}")
    return SingleEntityResponse(data=getting_promo(obj=obj))


if __name__ == "__main__":
    logging.info('Running...')
