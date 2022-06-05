
from this import d
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from App.database.db import db
from App.models import mongo_models
from App.Services import crud_mongo
from sqlalchemy import or_, and_
router = APIRouter(
    prefix="/api/home_slider",
    tags=['home_slider']
)


@router.get('')
async def get_students():
    students = await crud_mongo.home_slider_crud.retrieve_students()
    if students:
        return students
    return "Empty list returned"


@router.post('')
async def add(request: mongo_models.home_slider):
    return await crud_mongo.home_slider_crud.add(request)


@router.delete('/{id}')
def delete(id: str):
    return crud_mongo.home_slider_crud.delete(id)
