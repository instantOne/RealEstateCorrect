from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    password = user.password
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Real_object).offset(skip).limit(limit).all()


def create_user_item(db: Session, object: schemas.Object):
    db_item = models.Real_object(**object.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items_for_user(db: Session, email: str):
    return db.query(models.Real_object).filter(models.Real_object.owner == email).all()