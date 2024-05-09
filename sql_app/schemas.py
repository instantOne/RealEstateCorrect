from pydantic import BaseModel
from typing import Optional



class ObjectBase(BaseModel):
    name: str
    adress: str
    description: str
    price: float
    owner: str
    img_url: str | None = None

    class Config:
        from_attributes = True

class ObjectViews(ObjectBase):
    views: int

    class Config:
        from_attributes = True

class User(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class Object(ObjectBase):
    id: int


class ReviewBase(BaseModel):
    text: str
    rating: int
    object_id: int
    owner: str

class Review(ReviewBase):
    id: int


class PriceBase(BaseModel):
    object_id: int
    price: float

class Price(PriceBase):
    id: int