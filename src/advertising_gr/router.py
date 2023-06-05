import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from advertising_gr.crud import crud_ad_gr
from advertising_gr.getters import getting_ad_gr
from advertising_gr.schemas import AdvertisingGrCreate, AdvertisingGrUpdate

from core.response import SingleEntityResponse, ListOfEntityResponse, Meta
from database import get_async_session


router = APIRouter(
    prefix="/advertising_group",
    tags=["Advertising Group"]
)


@router.get('/all',
            response_model=ListOfEntityResponse,
            name='Список рекламируемых групп',
            description='Получение списка всех рекламируемых групп'
            )
async def get_ad_gr(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session),
):
    objects, code, indexes = await crud_ad_gr.get_all_ad_gr(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_ad_gr(obj) for obj in objects])


@router.get("/",
            response_model=SingleEntityResponse,
            name='Вывод рекламируемой группы по айди',
            description='Вывод рекламируемой группы по айди'
            )
async def get_ad_gr(
        ad_gr_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_ad_gr.get_ad_gr_by_id(db=session, ad_gr_id=ad_gr_id)
    # ошибки обработать
    if code != 0:
        return SingleEntityResponse(data=f"ERROR: {code}")
    return SingleEntityResponse(data=getting_ad_gr(obj=obj))


@router.post("/",
             response_model=SingleEntityResponse,
             name='Создать рекламируемую группу',
             description='Создать рекламируемую группу'
             )
async def create_ad_gr(
        new_data: AdvertisingGrCreate,
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_ad_gr.create_ad_gr(db=session, new_data=new_data)
    # ошибки обработать
    if code != 0:
        return SingleEntityResponse(data=f"ERROR: {code}")
    return SingleEntityResponse(data=getting_ad_gr(obj=obj))


@router.put("/",
            response_model=SingleEntityResponse,
            name='Изменить рекламируемую группу',
            description='Изменить рекламируемую группу'
            )
async def update_ad_gr(
        update_data: AdvertisingGrUpdate,
        ad_gr_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    obj, code, indexes = await crud_ad_gr.update_ad_gr(db=session,
                                                       update_data=update_data,
                                                       ad_gr_id=ad_gr_id)
    # ошибки обработать
    if code != 0:
        return SingleEntityResponse(data=f"ERROR: {code}")
    return SingleEntityResponse(data=getting_ad_gr(obj=obj))


if __name__ == "__main__":
    logging.info('Running...')
