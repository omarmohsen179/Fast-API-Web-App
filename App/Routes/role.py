
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from App.database.db import db
from App.models import schemas, models
from App.Services import crud
router = APIRouter(
    prefix="/api/role",
    tags=['role']
)


@router.get('')
def get_user(db: Session = Depends(db)):
    return crud.role_crud.get_all(db)


@router.post('')
def add(request: schemas.role, db: Session = Depends(db)):
    return crud.role_crud.add(db, models.role(Name=request.Name))


@router.post('/list')
def addlist(request: list[schemas.role], db: Session = Depends(db)):
    return crud.role_crud.add_list(db, request)


@router.put('')
def update(request: schemas.role, db: Session = Depends(db)):
    return crud.role_crud.update(db, request)


@router.delete('/{id}')
def delete(id: int, db: Session = Depends(db)):
    return crud.role_crud.delete(db, id)


@router.delete('/all/')
def delete(db: Session = Depends(db)):
    return crud.role_crud.delete_all(db)
