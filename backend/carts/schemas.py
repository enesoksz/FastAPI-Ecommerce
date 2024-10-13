from pydantic import BaseModel
from typing import List
from product.schemas import ProductCreate


class CartSummary(BaseModel):
    subtotal: float
    shipping_estimate: float
    tax_estimate: float
    total: float


class CartBase(BaseModel):
    products: List[ProductCreate]
    cart_summary: List[CartSummary]
