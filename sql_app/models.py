from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Identity
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=1,cycle=False), autoincrement = True)
    email = Column(String, primary_key=True, unique=True, index=True)
    password = Column(String)



class Real_object(Base):
    __tablename__ = "objects"

    id = Column(Integer, Identity(start=1,cycle=False), autoincrement=True, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    adress = Column(String, index=False)
    price = Column(Float)
    img_url = Column(String)
    owner = Column(String, ForeignKey("users.email"))