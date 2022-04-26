
from logging import exception
from sqlalchemy.orm import Session
from fastapi import APIRouter,  BackgroundTasks,  Depends, status, Body, UploadFile, File, HTTPException
from typing import List
from App.database import get_db
from starlette.responses import JSONResponse
from App import schemas, models
from App.Services import crud, image_uploader
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from App.Services.send_mail import *
router = APIRouter(
    prefix="/service",
    tags=['service']
)
db = get_db


class EmailSchema(BaseModel):
    email: List[EmailStr]


@router.get('/send-email/asynchronous')
async def send_email_asynchronous():
    await send_email_async('Hello World', ['Mohamedkoriam9999@gmail.com', "mohsenomar350@gmail.com"], {
        'title': 'Hello World hi thier',
        'name': 'John Doe hi thier'
    })
    return 'Success Mohamedkoriam9999@gmail.com'


@router.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks):
    send_email_background(background_tasks, 'Hello World', 'someemail@gmail.com', {
        'title': 'Hello World',
        'name': 'John Doe'
    })
    return 'Success'


@router.post("/upload-files")
async def cont_upload_files(files: List[UploadFile] = File(...)):
    image = (await image_uploader.upload_file(files))
    if not image.isOk:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=image.result)
    return image


@router.post("/upload-file")
async def cont_upload_file(file: UploadFile = File(...)):
    image = (await image_uploader.upload_file(file))
    if not image.isOk:
        return JSONResponse(status_code=400, content=image.dict())
    return JSONResponse(status_code=200, content=image.dict())
