from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, MetaData, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

from dish.models import Dish

metadata = MetaData()


class Cart(Base):
    __tablename__ = "cart"
    metadata = metadata

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, nullable=False)
    dish_id = Column(Integer, ForeignKey(Dish.id, ondelete="SET NULL"), nullable=True)
    amount = Column(Integer, nullable=False)
    sum = Column(Float, nullable=False)

    dish = relationship("Dish")
