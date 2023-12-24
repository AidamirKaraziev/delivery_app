from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Boolean, MetaData, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from database import Base

from order_status.models import OrderStatus
from selling_point.models import SellingPoint


metadata = MetaData()


class Order(Base):
    __tablename__ = "order"
    metadata = metadata

    id = Column(Integer, primary_key=True, autoincrement=True)
    selling_point_id = Column(Integer, ForeignKey(SellingPoint.id, ondelete="SET NULL"), nullable=True)
    
    cart = relationship("Cart", back_populates="order", uselist=False, lazy="joined")

    sum = Column(Integer, nullable=False, default=0)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    completed_at = Column(TIMESTAMP, nullable=True)
    # TODO rename status_id to order_status_id
    status_id = Column(Integer, ForeignKey(OrderStatus.id, ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    selling_point = relationship(SellingPoint, backref="orders", lazy="joined")
    status = relationship(OrderStatus, backref="orders", lazy="joined")
