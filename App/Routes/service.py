
from fastapi import APIRouter,  BackgroundTasks,  status, UploadFile, File, HTTPException
from typing import List
from App.Services.db import db
from starlette.responses import JSONResponse
from App.models import schemas
from App.Services import image_uploader
from pydantic import EmailStr, BaseModel
from App.Services.send_mail import *
router = APIRouter(
    prefix="/api/service",
    tags=['service']
)



class EmailSchema(BaseModel):
    email: List[EmailStr]


@router.get('/send-email/confirm')
async def send_email_asynchronous(body:schemas.template_body):
    body.buttonText="confirm"
    body.details="thanks for creating account. we hope you take good experiance with us"
    await send_email_async('Hello World', [ "mohsenomar350@gmail.com"], body)
    return 'Success'


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
