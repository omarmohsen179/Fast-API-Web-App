
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body
from App.database import get_db
from App import schemas, models
from App.Services.crud import ItemCrud
from App.security.Oauth import get_current_user
router = APIRouter(
    prefix="/item",
    tags=['item']
)
db = get_db


@router.get('')
def get_user(db: Session = Depends(db), current_user: schemas.User = Depends(get_current_user)):
    print(current_user)
    return ItemCrud.get_all(db)


@router.post('')
def createAccount(request: schemas.Item, db: Session = Depends(db)):
    return ItemCrud.add(db, models.Item(Name=request.Name))


@router.put('')
def createAccount(request: schemas.Item, db: Session = Depends(db)):
    return ItemCrud.update(db, models.Item(**request.dict()))


@router.delete('/{id}')
def createAccount(id: int, db: Session = Depends(db)):
    return ItemCrud.delete(db, id)
