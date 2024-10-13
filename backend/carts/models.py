from sqlalchemy import Column, ForeignKey, Integer, String, Float
from database import Base
from sqlalchemy.orm import relationship


class CartSummary(Base):
    __tablename__ = "cart_summary"

    id = Column(Integer, primary_key=True, index=True)
    subtotal = Column(Float, nullable=False)
    shipping_estimate = Column(Float, nullable=False)
    tax_estimate = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    cart_id = Column(Integer, ForeignKey("cart.id"))


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    summary = relationship("CartSummary", backref="cart", uselist=False)
    products = relationship("Product", backref="cart")
