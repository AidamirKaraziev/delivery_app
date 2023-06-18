from datetime import datetime


from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, MetaData, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select, func
from database import Base

from selling_point.models import SellingPoint
from cart.models import Cart
from status.models import Status

metadata = MetaData()


class Order(Base):
    __tablename__ = "order"
    metadata = metadata

    id = Column(Integer, primary_key=True)
    selling_point_id = Column(Integer, ForeignKey(SellingPoint.id, ondelete="SET NULL"), nullable=True)
    cart_id = Column(Integer, ForeignKey(Cart.cart_id, ondelete="SET NULL"), nullable=True)

    amount = Column(Integer, nullable=False)
    sum = Column(Integer, nullable=False, default=0)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    completed_at = Column(TIMESTAMP, nullable=True)

    status_id = Column(Integer, ForeignKey(Status.id, ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    selling_point = relationship("SellingPoint", backref="selling_points", lazy="joined")
    cart = relationship("Cart", lazy="joined")
    status = relationship("Status", lazy="joined")

    @staticmethod
    async def calculate_sum(cart_id, async_session):
        subquery = select(func.sum(Cart.sum)).where(Cart.cart_id == cart_id).scalar_subquery()
        async with async_session() as session:
            result = await session.execute(subquery)
            return result.scalar()

    # Пример использования функции для расчета суммы
    # async with get_async_session() as session:
    #     order_sum = await Order.calculate_sum(cart_id, session)





