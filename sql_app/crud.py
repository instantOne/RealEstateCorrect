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
    db_prices = models.Price_history()
    db_objs = db.query(models.Real_object).filter(models.Real_object.owner == db_item.owner).all()
    records = [record.id for record in db_objs]
    db_prices.object_id = records[-1]
    db_prices.price = db_item.price
    db.add(db_prices)
    db.commit()
    db.refresh(db_prices)
    return db_item

def get_items_for_user(db: Session, email: str):
    return db.query(models.Real_object).filter(models.Real_object.owner == email).all()

def change_item_by_id(db: Session, id: int, object: schemas.ObjectBase):
    db_object = db.query(models.Real_object).filter(models.Real_object.id == id).first()
    #Добавить условия для изменения цены(если цена неизменная, не добавлять в таблицу Prices новую)
    for attr, value in object.model_dump().items():
        setattr(db_object, attr, value)
    db_prices = models.Price_history()
    db_prices.object_id = id
    db_prices.price = db_object.price
    db.add(db_prices)
    db.commit()
    db.refresh(db_object)
    db.refresh(db_prices)
    return db_object

def create_review_for_object(db: Session, object: schemas.ReviewBase):
    db_item = models.Review(**object.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_by_id(db: Session, id: int) -> schemas.Object:
    db_object = db.query(models.Real_object).filter(models.Real_object.id == id).first()
    db_object.views += 1
    db.commit()
    db.refresh(db_object)
    return db_object

def get_avg_price(db: Session, id: int):
    db_object = db.query(models.Price_history).filter(models.Price_history.object_id == id).all()
    prices = [elem.price for elem in db_object]
    return sum(prices) / len(prices)


