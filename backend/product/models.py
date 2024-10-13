from sqlalchemy import Column, ForeignKey, Integer, String, Float
from database import Base
from typing import Dict
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    color = Column(String)
    size = Column(String)
    quantity = Column(Integer)

    cart_id = Column(Integer, ForeignKey("cart.id"))
