
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body
from App.database import get_db
from App import schemas, models
from App.Services.auth import create, login
from App.Services.crud import UserCrud
router = APIRouter(
    prefix="/auth",
    tags=['auth']
)
db = get_db


@router.get('/')
def get_user(db: Session = Depends(db)):
    x = UserCrud.get_all(db)
    return x


@router.post('/create-account')
def createAccount(request: schemas.CreateAccount, db: Session = Depends(db)):
    return create(request, db)


@router.post('/login')
def Login(request: schemas.LoginForm, db: Session = Depends(db)):
    return login(request, db)
