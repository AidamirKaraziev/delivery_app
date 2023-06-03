from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean

from src.database import Base


class Role(Base):
    __tablename__ = "role"
    metadata = Base.metadata

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)
