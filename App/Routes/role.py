
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from App.database import get_db
from App import schemas, models
from App.Services import crud
router = APIRouter(
    prefix="/role",
    tags=['role']
)
db = get_db


@router.get('')
def get_user(db: Session = Depends(db)):
    return crud.RoleCrud.get_all(db)


@router.post('')
def add(request: schemas.Role, db: Session = Depends(db)):
    return crud.RoleCrud.add(db, models.Role(Name=request.Name))


@router.post('/list')
def addlist(request: list[schemas.Role], db: Session = Depends(db)):
    values = list(map(lambda e: models.Role(**e.dict()), request))
    return crud.RoleCrud.add_list(db, values)


@router.put('')
def update(request: schemas.Role, db: Session = Depends(db)):
    return crud.RoleCrud.update(db, models.Role(**request.dict()))


@router.delete('/{id}')
def delete(id: int, db: Session = Depends(db)):
    return crud.RoleCrud.delete(db, id)


@router.delete('/all/')
def delete(db: Session = Depends(db)):
    return crud.RoleCrud.delete_all(db)
