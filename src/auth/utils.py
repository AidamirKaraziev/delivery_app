from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session

from auth.models import User
from database import get_session


def get_user_db(session: Session = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
