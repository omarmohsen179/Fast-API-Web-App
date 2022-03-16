
from sqlalchemy.orm import Session
from fastapi import APIRouter
from App.models import User
router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


def GetAll(db):
    return db.query(User).all()
