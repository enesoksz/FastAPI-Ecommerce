from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from database import get_db
from sqlalchemy.orm import Session
from .models import CartSummary, Cart
from .schemas import CartBase, CartSummary
from typing import List

router = APIRouter(tags=["Carts"], prefix="/carts")


@router.get("")
async def get_cart(db: Session = Depends(get_db)):
    cart = db.query(Cart).all()
    print(cart)
    return cart


@router.post("")
async def update_cart(cart: CartBase, db: Session = Depends(get_db)):
    if not cart.products:
        raise HTTPException(status_code=400, detail="Cart cannot be empty")

    subtotal = sum(item.price * item.quantity for item in cart.products)

    shipping_estimate = 11.00
    tax_estimate = subtotal * 0.1

    total = subtotal + shipping_estimate + tax_estimate

    cart.cart_summary = [
        CartSummary(
            subtotal=subtotal,
            shipping_estimate=shipping_estimate,
            tax_estimate=tax_estimate,
            total=total,
        )
    ]

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart
