
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body
from App.database import get_db
from App import schemas, models
from App.services.crud import Role
from App.security.Oauth import get_current_user
router = APIRouter(
    prefix="/role",
    tags=['role']
)
db = get_db


@router.get('')
def get_user(db: Session = Depends(db), current_user: schemas.User = Depends(get_current_user)):
    print(current_user)
    return Role.get_all(db)


@router.post('')
def createAccount(request: schemas.Item, db: Session = Depends(db)):
    return Role.add(db, models.Item(Name=request.Name))


@router.put('')
def createAccount(request: schemas.Item, db: Session = Depends(db)):
    return Role.update(db, models.Item(**request.dict()))


@router.delete('/{id}')
def createAccount(id: int, db: Session = Depends(db)):
    return Role.delete(db, id)
