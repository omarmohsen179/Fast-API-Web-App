
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Body, UploadFile, File
from typing import List
from App.database import get_db
from App import schemas, models
from App.Services.crud import ItemCrud
from App.security.Oauth import get_current_user
import os
import logging
import aiofiles
router = APIRouter(
    prefix="/item",
    tags=['item']
)
db = get_db

async def chunked_copy(src, dst):
    await src.seek(0)
    with open(dst, "wb") as buffer:
        while True:
            contents = await src.read(2 ** 20)
            if not contents:
                break
            buffer.write(contents)


@router.post("/upload-files")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        destination_file_path = "/home/fm-pc-lt-46/Music/" + \
            file.filename  # output file path
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read file chunk
                await out_file.write(content)  # async write file chunk
    return {"Result": "OK", "filenames": [file.filename for file in files]}


@router.post("/upload-file")
async def create_upload_file(file: UploadFile = File(...)):
    fullpath = os.path.join("D:/Code/python/Fast-API-Web-App/", file.filename)
    await chunked_copy(file, fullpath)
    return {"File saved to disk at": fullpath}


@router.get('')
def get_user(db: Session = Depends(db), current_user: schemas.User = Depends(get_current_user)):
    print(current_user)
    return ItemCrud.get_all(db)


@router.post('')
def createAccount(request: schemas.Item, db: Session = Depends(db)):
    return ItemCrud.add(db, models.Item(Name=request.Name))


@router.put('')
def createAccount(request: schemas.Item, db: Session = Depends(db)):
    return ItemCrud.update(db, models.Item(**request.dict()))


@router.delete('/{id}')
def createAccount(id: int, db: Session = Depends(db)):
    return ItemCrud.delete(db, id)
