
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body
from App.database import get_db
from App import schemas, models
from App.services.auth import create, login

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)
db = get_db


@router.get('/')
def get_user(db: Session = Depends(db)):
    return models.UserCrud().get_all(db)


@router.post('/create-account')
def createAccount(request: schemas.User, db: Session = Depends(db)):
    return create(request, db)


@router.post('/login')
def Login(request: schemas.LoginForm, db: Session = Depends(db)):
    return login(request, db)
