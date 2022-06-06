
from email.mime import image
from this import d
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File
from App.database.db import db
from App.Services import image_uploader
from fastapi import APIRouter,  BackgroundTasks,  status, UploadFile, File, HTTPException
from App.models import mongo_models
from App.Services import crud_mongo
from sqlalchemy import or_, and_
router = APIRouter(
    prefix="/api/home_slider",
    tags=['home_slider']
)


@router.get('')
async def get_students():
    try:
        return await crud_mongo.home_slider_crud.get()
    except Exception as ex:
        return ex


@router.post('')
async def add(image: UploadFile = File(...)):
    image = (await image_uploader.upload_file(image))
    return await crud_mongo.home_slider_crud.add(mongo_models.home_slider(image_path=image.result))


@router.delete('/{id}')
def delete(id: str):
    return crud_mongo.home_slider_crud.delete(id)
