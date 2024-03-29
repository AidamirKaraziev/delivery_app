from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, MetaData
from sqlalchemy.orm import relationship
from database import Base

from promo.models import Promo

metadata = MetaData()


class Dish(Base):
    __tablename__ = "dish"
    metadata = metadata

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    main_photo = Column(String, nullable=True)
    photo_1 = Column(String, nullable=True)
    photo_2 = Column(String, nullable=True)

    description = Column(String, nullable=True)
    composition = Column(String, nullable=True)
    price = Column(Integer, nullable=False)

    promo_id = Column(Integer, ForeignKey(Promo.id, ondelete="SET NULL"), nullable=True)
    visible = Column(Boolean, nullable=False)
    is_active = Column(Boolean, default=True)

    promo = relationship(Promo, backref="promos", lazy="joined")


