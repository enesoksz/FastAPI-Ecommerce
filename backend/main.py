from fastapi import FastAPI, Depends, HTTPException, status
from database import SessionLocal, engine
from pydantic import BaseModel
from auth.models import User, Base
from sqlalchemy.orm import Session
from product.router import router as product_router
from auth.router import router as auth_router
from carts.router import router as carts_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(carts_router)
