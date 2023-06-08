from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, MetaData
from sqlalchemy.orm import relationship
from database import Base

from promo.models import Promo

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

    promo_id = Column(Integer, ForeignKey(Promo.id, ondelete="SET NULL"), nullable=True)
    visible = Column(Boolean, nullable=False)

    promo = relationship("Promo", backref="dishes", lazy="joined")

    is_active = Column(Boolean, default=True, nullable=False)
