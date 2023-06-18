from datetime import datetime
from passlib.hash import bcrypt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.auth.models import User
from src.role.models import Role
from src.database import get_async_session

from config import SUPERUSER_EMAIL
from config import SUPERUSER_PASSWORD


async def check_roles(session: AsyncSession = Depends(get_async_session)):
    # Проверяем наличие ролей
    query_admin = select(Role).where(Role.name == 'admin')
    query_user = select(Role).where(Role.name == 'user')

    admin_role = await session.execute(query_admin)
    user_role = await session.execute(query_user)

    if admin_role.scalar_one_or_none() is not None:
        admin_role_is_exist = True
    else:
        admin_role_is_exist = False

    if user_role.scalar_one_or_none() is not None:
        user_role_is_exist = True
    else:
        user_role_is_exist = False

    return admin_role_is_exist, user_role_is_exist


async def chech_superuser(session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.name == 'superuser')
    superuser = await session.execute(query)
    if superuser.scalar_one_or_none() is not None:
        return True
    return False


async def create_roles():
    async for db in get_async_session():
        roles = []

        # Проверка наличия данных
        admin_role_is_exist, user_role_is_exist = await check_roles(db)

        if admin_role_is_exist and user_role_is_exist:
            return  # Начальные данные уже существуют

        # Создание недостающих ролей
        if not admin_role_is_exist:
            roles.append(Role(name='admin', permissions=None))
        if not user_role_is_exist:
            roles.append(Role(name='user', permissions=None))

        [db.add(role) for role in roles]
        await db.commit()
        await db.close()


async def crete_superuser():
    async for db in get_async_session():

        # Проверка наличия данных
        superuser_exists = await chech_superuser(db)
        if superuser_exists:
            return  # Начальные данные уже существуют

        # Получаем role_id
        query_admin = select(Role).where(Role.name == 'admin')
        responce = await db.execute(query_admin)

        admin = responce.scalar_one_or_none()
        hashed_password = bcrypt.hash(SUPERUSER_PASSWORD)

        # Создание пользователей
        superuser = User(
            name='superuser',
            photo='path_to_photo',
            email=SUPERUSER_EMAIL,
            phone_number='0',
            registered_at=datetime.utcnow(),
            hashed_password=hashed_password,
            role_id=admin.id,
            is_active=True,
            is_superuser=True,
            is_verified=True
        )

        db.add(superuser)
        await db.commit()
        await db.close()


async def create_initial_data():
    await create_roles()
    await crete_superuser()
