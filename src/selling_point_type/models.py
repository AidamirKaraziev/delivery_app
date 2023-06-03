from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class SellingPointType(Base):
    __tablename__ = "selling_point_type"
    metadata = Base.metadata

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    #svg???
