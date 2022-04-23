
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body
from App.database import get_db
from App import schemas, models
from App.services.auth import create, login
from App.services.crud import UserCrud, RoleCrud
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from App.security.Oauth import get_current_user, get_current_admin
routerauth = APIRouter(
    prefix="/auth",
    tags=['auth']
)
db = get_db


@routerauth.get('/')
def get_user(db: Session = Depends(db)):
    json_compatible_item_data = jsonable_encoder(
        list(map(lambda e: schemas.User(**dict(e.__dict__), Role=e.Roles.Name), UserCrud.get_all(db))))
    # return list(map(getvalue, UserCrud.get_all(db)))
    return JSONResponse(content=json_compatible_item_data)


@routerauth.post('/create-account')
def createAccount(request: schemas.CreateAccount, db: Session = Depends(db)):
    return create(request, db)


@routerauth.post('/login')
def Login(request: schemas.LoginForm, db: Session = Depends(db)):
    return login(request, db)


@routerauth.get('/admin')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(get_current_admin)):
    return "admin"


@routerauth.get('/user')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(get_current_user)):
    return "user"


@routerauth.delete('/{id}')
def createAccount(id: int, db: Session = Depends(db)):
    return UserCrud.delete(db, id)


@routerauth.delete('/all/')
def createAccount(db: Session = Depends(db)):
    return UserCrud.delete_all(db)
