
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body
from App.database import get_db
from App import schemas, models
from App.Services import crud, auth

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from App.security.Oauth import get_current_user, get_current_admin
Routerauth = APIRouter(
    prefix="/auth",
    tags=['auth']
)
db = get_db


@Routerauth.get('/')
def get_user(db: Session = Depends(db)):
    json_compatible_item_data = jsonable_encoder(
        list(map(lambda e: schemas.User(**dict(e.__dict__), Role=e.Roles.Name), UserCrud.get_all(db))))
    # return list(map(getvalue, UserCrud.get_all(db)))
    return JSONResponse(content=json_compatible_item_data)


@Routerauth.post('/create-account')
def createAccount(request: schemas.CreateAccount, db: Session = Depends(db)):
    return auth.create(request, db)


@Routerauth.post('/login')
def Login(request: schemas.LoginForm, db: Session = Depends(db)):
    return auth.login(request, db)


@Routerauth.get('/admin')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(get_current_admin)):
    return "admin"


@Routerauth.get('/user')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(get_current_user)):
    return "user"


@Routerauth.delete('/{id}')
def createAccount(id: int, db: Session = Depends(db)):
    return crud.UserCrud.delete(db, id)


@Routerauth.delete('/all/')
def createAccount(db: Session = Depends(db)):
    return crud.UserCrud.delete_all(db)
