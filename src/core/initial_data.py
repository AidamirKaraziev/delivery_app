from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from config import STATUS_CREATE, STATUS_IN_PROCESS, STATUS_DONE, ROLE_ADMIN, ROLE_USER
from order_status.models import OrderStatus
from role.models import Role
from database import get_async_session


async def check_status(session: AsyncSession = Depends(get_async_session)):
    check_list = [
        OrderStatus(id=STATUS_CREATE.id, name=STATUS_CREATE.name),
        OrderStatus(id=STATUS_IN_PROCESS.id, name=STATUS_IN_PROCESS.name),
        OrderStatus(id=STATUS_DONE.id, name=STATUS_DONE.name)
                  ]
    creation_list = []
    for obj in check_list:
        query = select(OrderStatus).where(OrderStatus.name == obj.name, OrderStatus.id == obj.id)
        obj_type = await session.execute(query)
        if obj_type.scalar_one_or_none() is None:
            creation_list.append(obj)
    return creation_list


async def create_statuses():
    async for db in get_async_session():
        creation_list = await check_status(db)
        [db.add(obj) for obj in creation_list]
        await db.commit()
        await db.close()


async def check_role(session: AsyncSession = Depends(get_async_session)):
    check_list = [
        Role(id=ROLE_ADMIN.id, name=ROLE_ADMIN.name),
        Role(id=ROLE_USER.id, name=ROLE_USER.name)
                  ]
    creation_list = []
    for obj in check_list:
        query = select(Role).where(Role.name == obj.name, Role.id == obj.id)
        obj_type = await session.execute(query)
        if obj_type.scalar_one_or_none() is None:
            creation_list.append(obj)
    return creation_list


async def create_roles():
    async for db in get_async_session():
        creation_list = await check_status(db)
        [db.add(obj) for obj in creation_list]
        await db.commit()
        await db.close()


async def create_initial_data():
    try:
        await create_roles()
    except Exception as e:
        print(e)
    try:
        await create_statuses()
    except Exception as e:
        print(e)
