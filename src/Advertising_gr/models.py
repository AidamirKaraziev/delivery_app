from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean

from database import Base, metadata


class AdvertisingGr(Base):
    __tablename__ = "advertising_gr"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
