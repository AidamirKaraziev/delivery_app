import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.response import SingleEntityResponse, ListOfEntityResponse
from database import get_async_session
from selling_point.crud import crud_selling_point
from selling_point.getters import getting_selling_point
from selling_point.schemas import SellingPointCreate, SellingPointUpdate


router = APIRouter(
    prefix="/selling_point",
    tags=["SellingPoint"]
)


@router.get(
    path='/selling_points',
    response_model=ListOfEntityResponse,
    name='get_selling_points',
    description='Получение списка точек сбыта'
)
async def get_selling_points(
        limit: int = 100,
        skip: int = 0,
        session: AsyncSession = Depends(get_async_session),
):
    selling_points, code, indexes = await crud_selling_point.get_all_selling_points(db=session, skip=skip, limit=limit)

    return ListOfEntityResponse(data=[getting_selling_point(selling_point) for selling_point in selling_points])


@router.get(
    path="/{selling_point_id}",
    response_model=SingleEntityResponse,
    name='get_selling_point_by_id',
    description='Вывод точки сбыта по идентификатору'
)
async def get_selling_point_by_id(
        selling_point_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    selling_point, code, indexes = await crud_selling_point.get_selling_point_by_id(db=session,
                                                                                    selling_point_id=selling_point_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return SingleEntityResponse(data=getting_selling_point(selling_point))


@router.post(
    path="/",
    response_model=SingleEntityResponse,
    name='create_selling_point',
    description='Добавление точки сбыта'
)
async def create_selling_point(
        new_data: SellingPointCreate,
        session: AsyncSession = Depends(get_async_session),
):
    selling_point, code, indexes = await crud_selling_point.create_selling_point(db=session, new_data=new_data)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=409, detail="Resource already exists")
    return SingleEntityResponse(data=getting_selling_point(selling_point))


@router.put(
    path="/{selling_point_id}",
    response_model=SingleEntityResponse,
    name='update_selling_point',
    description='Изменить точку сбыта'
)
async def update_selling_point(
        update_data: SellingPointUpdate,
        selling_point_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    selling_point, code, indexes = await crud_selling_point.update_selling_point(db=session,
                                                                                 update_data=update_data,
                                                                                 selling_point_id=selling_point_id)
    # ошибки обработать
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return SingleEntityResponse(data=getting_selling_point(selling_point=selling_point))


@router.delete(
    path='/{selling_point_id}',
    response_model=SingleEntityResponse,
    name='delete_selling_point',
    description='Удалить точку сбыта'
)
async def delete_selling_point(
        selling_point_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    selling_point, code, indexes = await crud_selling_point.delete_selling_point(db=session,
                                                                                 selling_point_id=selling_point_id)
    if code != 0:
        raise HTTPException(status_code=404, detail="Resource with this ID does not exist")
    return SingleEntityResponse(data=getting_selling_point(selling_point=selling_point))


if __name__ == "__main__":
    logging.info('Running...')
