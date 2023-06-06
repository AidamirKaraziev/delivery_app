from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from database import Base

from auth.models import User
from selling_point_type.models import SellingPointType

metadata = MetaData()


class SellingPoint(Base):
    __tablename__ = "selling_point"
    metadata = metadata

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    photo = Column(String, nullable=True)

    selling_point_type_id = Column(Integer, ForeignKey(SellingPointType.id, ondelete="SET NULL"))

    address = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey(User.id, ondelete="SET NULL"))

    user = relationship(User, backref="users", lazy="joined")
    type = relationship(SellingPointType, backref="selling_point_types", lazy="joined")
