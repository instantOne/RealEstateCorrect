from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

#получение списка user'ов
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#получение юхера по email
@app.get("/users/{email}", response_model=schemas.User)
def read_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#добавление объекта
@app.post("/user/add/object/", response_model=schemas.ObjectBase)
def create_item_for_user(
    owner: str, object: schemas.ObjectBase, db: Session = Depends(get_db)
):
    object.owner = owner #костыль
    return crud.create_user_item(db, object=object)

#получение всех доступных объектов (опционально с шагом)
@app.get("/items/", response_model=List[schemas.Object])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
# получение объектов по email для конкретного пользователя
@app.get("/items/{email}", response_model=List[schemas.Object])
def read_items_for_user(email: str, db: Session = Depends(get_db)):
    items = crud.get_items_for_user(db, email)
    return items

#Изменение объекта по id
@app.post("/items/change/{id}")
async def change_item_by_id(object: schemas.ObjectBase, id: int, db: Session = Depends(get_db)):
    item = crud.change_item_by_id(db, id, object=object)

    return item


