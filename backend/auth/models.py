from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel
from utils import get_password_hash, verify_password
from typing import Dict


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
