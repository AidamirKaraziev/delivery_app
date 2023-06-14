import logging
import shutil
import time
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status, UploadFile, File
from fastapi.responses import FileResponse
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.manager import BaseUserManager
from fastapi_users import exceptions, models
from fastapi.staticfiles import StaticFiles

from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserCreate, UserGet, UserRead
from core.response import ListOfEntityResponse, SingleEntityResponse
from database import get_async_session

from user.crud import crud_user
from user.getters import getting_user
from sqlalchemy import exc, select, delete, update

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "upload")

timestr = time.strftime("%Y%m%d-%H%M%S")

PATH_MODEL = "user"
PATH_PHOTO = "photo"

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
        request: Request,
        skip: int = 0,
        limit: int = 100,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    objects, code, indexes = await crud_user.get_all_users(db=session, skip=skip, limit=limit)
    return ListOfEntityResponse(data=[getting_user(obj, request=request) for obj in objects])


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


@router.get("/test/")
def read_root():
    return {"hellow": "AIDAMIR"}


@router.post('file/upload/')
async def upload_file(file: UploadFile):
    if file.content_type != "image/png" and "image/jpeg":
        return HTTPException(status_code=400, detail=f"invalid content type {file.content_type}")
    return {"content": file.file, "filename": file.filename, "size": file.size, "content_type": file.content_type}


@router.post("/file/upload-download/")
async def upload_n_download(file: UploadFile):
    if file.content_type != "image/png" and "image/jpeg":
        return HTTPException(status_code=400, detail=f"invalid content type {file.content_type}")
    new_filename = file.filename
    # new_filename = "{}_{}".format(os.path.splitext(file.filename)[0], timestr)
    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)
    with open(SAVE_FILE_PATH, "wb") as wf:
        shutil.copyfileobj(file.file, wf)
        file.file.close()

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_filename)


router.mount("/static", StaticFiles(directory="static"), name="static")


@router.put("/me/add-photo/",
            response_model=SingleEntityResponse,
            name='add_photo',
            description='Добавить фото'
            )
async def add_photo(
        request: Request,
        file: Optional[UploadFile] = File(None),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
        ):
    save_path = await crud_user.adding_file(
        db=session, file=file, path_model=PATH_MODEL,
        path_type=PATH_PHOTO, db_obj=user, base_path="./static/")
    if not save_path:
        return HTTPException(status_code=400, detail=f"Not have save photo")
    return SingleEntityResponse(data=getting_user(user, request=request))


if __name__ == "__main__":
    logging.info('Running...')
