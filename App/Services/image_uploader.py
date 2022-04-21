
from fastapi import APIRouter, Depends, status, Body, UploadFile, File
import os
from typing import List
import uuid
from PIL import Image
import filetype
from App.schemas import ImageResponse


async def chunked_copy(src: UploadFile):

    if not src.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise ValueError("invalid file")
    (file_name, extension) = os.path.splitext(src.filename)
    filename = uuid.uuid4().hex+extension
    fullpath = os.path.join(os.getcwd()+"/static/", filename)
    await src.seek(0)
    with open(fullpath, "wb") as buffer:
        while True:
            contents = await src.read(2 ** 20)
            if not contents:
                break
            buffer.write(contents)
    return "/static/" + filename


async def upload_file(file: UploadFile = File(...)) -> ImageResponse:
    try:
        return ImageResponse(isOk=True, result=(await chunked_copy(file)))
    except Exception as error:
        return ImageResponse(isOk=False, result=error.args[0])


async def upload_files(files: List[UploadFile] = File(...)) -> ImageResponse:
    try:
        files = []
        for i in files:
            files.append((await chunked_copy(i)))
        return ImageResponse(isOk=True, result=files)
    except Exception as error:
        return ImageResponse(isOk=False, result=error.args[0])
