from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, status
from database import SessionLocal, engine
from pydantic import BaseModel, EmailStr
from auth.models import User, Base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
import auth.router as router
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import LoginForm, UserCreate

router = APIRouter(tags=["User"])


@router.get("/user")
def read_user(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/register")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return {"message": "User already exists", "user_id": existing_user.id}

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "user_id": new_user.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="This email already exists.")


@router.post("/login")
def login(form_data: LoginForm, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
