from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData

from src.database import Base
from src.role.models import Role


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    metadata = Base.metadata

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=False)

    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)

    hashed_password: str = Column(String(length=1024), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id", ondelete="SET NULL"))
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
