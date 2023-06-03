from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class SellingPoint(Base):
    __tablename__ = "selling_point"
    metadata = Base.metadata

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    photo = Column(String, nullable=True)

    sp_type_id = Column(Integer, ForeignKey("selling_point_type.id", ondelete="SET NULL"))

    address = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey("user.id", ondelete="SET NUL"))
