from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, MetaData
from database import Base

from advertising_gr.models import AdvertisingGr

metadata = MetaData()


class Dish(Base):
    __tablename__ = "dish"
    metadata = metadata

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    main_photo = Column(String, nullable=False)
    photo1 = Column(String, nullable=True)
    photo2 = Column(String, nullable=True)

    discription = Column(String, nullable=True)
    composition = Column(String, nullable=True)
    price = Column(Float, nullable=False)


    advertising_gr_id = Column(Integer, ForeignKey(AdvertisingGr.id, ondelete="SET NULL"))
