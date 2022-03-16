
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body
from App.database import get_db
from App.Services.crud import GetAll
from App import schemas, models
from App.Services.auth import create

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)
db = get_db


class auth:
    @router.get('')
    def get_user(db: Session = Depends(db)):
        return GetAll(db)

    @router.post('/create-account')
    def createAccount(request: schemas.User, db: Session = Depends(db)):
        return create(request, db)
