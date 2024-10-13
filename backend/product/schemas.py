from pydantic import BaseModel


class ProductCreate(BaseModel):
    id: int
    name: str
    price: float
    color: str
    size: str | None = None
    quantity: int
