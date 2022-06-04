
from fastapi import APIRouter,  BackgroundTasks,  status, UploadFile, File, HTTPException
from this import d
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from App.database.db import db
from App.models import schemas, models
from App.Services import crud
router = APIRouter(
    prefix="/api/category",
    tags=['category']
)


@router.get('')
def get_user(db: Session = Depends(db)):
    return crud.categories_crud.get(db).all()


@router.get('/{id}')
def get_user(id: int, db: Session = Depends(db)):
    return crud.item_crud.get_filter(db, models.item == id).all()


@router.post('')
def add(request: schemas.categories, db: Session = Depends(db)):
    del request.Id
    temp = models.item_category(**request.dict())
    print(temp)
    return crud.categories_crud.add(db, temp)


@router.post('/list')
def addlist(request: list[schemas.categories], db: Session = Depends(db)):
    values = list(map(lambda e: models.item_category(**e.dict()), request))
    return crud.categories_crud.add_list(db, values)


@router.put('')
def update(request: schemas.categories, db: Session = Depends(db)):
    return crud.categories_crud.update(db, request)


@router.delete('/{id}')
def delete(id: int, db: Session = Depends(db)):
    return crud.categories_crud.delete(db, id)


@router.delete('/all/')
def delete(db: Session = Depends(db)):
    return crud.categories_crud.delete_all(db)
