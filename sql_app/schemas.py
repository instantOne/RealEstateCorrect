from pydantic import BaseModel
from typing import Optional



class ObjectBase(BaseModel):
    name: str
    adress: str
    description: str
    price: float
    img_url: str | None = None

    class Config:
        from_attributes = True


class User(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class Object(ObjectBase):
    id: int
    owner: str
