import glob
import os
import shutil
import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

# from app.db.base_class import Base
# from app.core.response import Paginator
# from app.utils import pagination


from core.exception import UnprocessableEntity, UnfoundEntity
from database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    # def get(self, db: Session, id: Any) -> Optional[ModelType]:
    #     return db.query(self.model).filter(self.model.id == id).first()

    # def get_multi(
    #     self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[ModelType]:
    #     return db.query(self.model).offset(skip).limit(limit).all()
    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        # session: AsyncSession = Depends(get_async_session)
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.first()
    # def get_multi(
    #         self, db: Session, *, page: Optional[int] = None
    # ) -> Tuple[List[ModelType], Paginator]:
    #
    #     query = db.query(self.model)
    #     return pagination.get_page(query, page)

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_for_user(
            self,
            db: Session,
            obj_in: CreateSchemaType,
            user_field_value: Any,
            user_field_name: str = "user"
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model({**obj_in_data, user_field_name: user_field_value})  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_by_name(self, db: Session, name: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.name == name).first()

    def adding_file(self, db: Session, *, file: Optional[UploadFile], path_model: str, path_type: str,
                    db_obj: ModelType):
        BASE_PATH = './static/'
        all_path = BASE_PATH + path_model + "/" + str(db_obj.id) + "/" + path_type + "/"
        if path_type not in db_obj.__dict__.keys():
            raise UnprocessableEntity(
                message="Модель в базе данных не имеет такого атрибута для файла!",
                num=108,
                description="Модель в базе данных не имеет такого атрибута для файла!",
                path="$.body"
            )
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = all_path + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({path_type: None})
            db.commit()
            return {path_type: None}
        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        element = [path_model, str(db_obj.id), path_type, filename]

        path_for_db = "/".join(element)

        if not os.path.exists(all_path):
            os.makedirs(all_path)

        # Удаляем все содержимое папки
        path_to_clear = all_path + "*"
        for file_to_clear in glob.glob(path_to_clear):
            os.remove(file_to_clear)

        with open(all_path + filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()  # удаляет временный

        db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({path_type: path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(
                message="Не отправлен загружаемый файл",
                num=2,
                description="Попробуйте загрузить файл еще раз",
                path="$.body",
            )
        else:
            return {path_type: path_for_db}

    def archiving(self,  db: Session, *, db_obj: ModelType):
        db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({"is_actual": False})
        db.commit()
        return db_obj, 0, None

    def unzipping(self,  db: Session, *, db_obj: ModelType):
        db.query(db_obj.__class__).filter(db_obj.__class__.id == db_obj.id).update({"is_actual": True})
        db.commit()
        return db_obj, 0, None

    def check_list(self, verify_list: list, all_list: list):
        for element in verify_list:
            if element not in all_list:
                return -109
            else:
                return 0
