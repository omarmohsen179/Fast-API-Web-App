
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from App.database import get_db
from App import schemas
from App.Services import crud, auth

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from App.security import Oauth
router = APIRouter(
    prefix="/auth",
    tags=['auth']
)
db = get_db


@router.get('/')
def get_user(db: Session = Depends(db)):
    json_compatible_item_data = jsonable_encoder(
        list(map(lambda e: schemas.User(**dict(e.__dict__), Role=e.Roles.Name), crud.UserCrud.get_all(db))))
    # return list(map(getvalue, UserCrud.get_all(db)))
    return JSONResponse(content=json_compatible_item_data)


@router.post('/create-account')
def createAccount(request: schemas.CreateAccount, db: Session = Depends(db)):
    return auth.create(request, db)


@router.post('/login')
def Login(request: schemas.LoginForm, db: Session = Depends(db)):
    return auth.login(request, db)


@router.get('/admin')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(Oauth.get_current_admin)):
    return "admin"


@router.get('/user')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(Oauth.get_current_user)):
    return "user"


@router.delete('/{id}')
def createAccount(id: int, db: Session = Depends(db)):
    return crud.UserCrud.delete(db, id)


@router.delete('/all/')
def createAccount(db: Session = Depends(db)):
    return crud.UserCrud.delete_all(db)
