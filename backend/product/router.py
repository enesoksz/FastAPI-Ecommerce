from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .models import Product
from database import get_db
from .schemas import ProductCreate
from typing import Annotated

router = APIRouter(tags=["Product"])


@router.get("/products")
def get_products(
    product: Annotated[list[str] | None, Query()] = None,
    db: Session = Depends(get_db),
):
    product = db.query(Product).all()
    return {"products": product}


@router.get("/products/{product_id}")
def get_products(
    product_id: Annotated[int, Path(title="The ID of the product to get")],
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    return product


@router.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name, price=product.price, color=product.color, size=product.size
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
