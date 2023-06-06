from sqlalchemy import Column, Integer, String, MetaData
from database import Base

metadata = MetaData()


class SellingPointType(Base):
    __tablename__ = "selling_point_type"
    metadata = metadata

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=True)
