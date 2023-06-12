import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users import exceptions, models, schemas


from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserCreate, UserGet, UserRead
from core.response import ListOfEntityResponse, SingleEntityResponse
from database import get_async_session

from user.crud import crud_user
from user.getters import getting_user

current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get(
            path='/all/',
            response_model=ListOfEntityResponse,
            name='get_users',
            description='Получение списка всех рекламируемых групп'
            )
async def get_users(
        skip: int = 0,
        limit: int = 100,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    objects, code, indexes = await crud_user.get_all_users(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_user(obj) for obj in objects])


@router.post(
    path="/create-admin/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    name="create_admin",
    description="Создание админа",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def create_admin(
    request: Request,
    user_create: UserCreate,  # type: ignore
    user: User = Depends(current_active_superuser),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        created_user = await user_manager.create_admin(
            user_create, safe=True, request=request
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    # create_user - это User, как вывести в getting_user() SingleEntityResponse
    return UserRead.from_orm(created_user)
    # return SingleEntityResponse(data=getting_user(obj=created_user))


if __name__ == "__main__":
    logging.info('Running...')
