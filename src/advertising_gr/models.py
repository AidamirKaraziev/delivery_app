from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean

from src.database import Base, metadata


class AdvertisingGr(Base):
    __tablename__ = "advertising_gr"

    metadata = metadata
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
