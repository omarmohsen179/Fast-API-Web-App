
from typing import List
from bson import ObjectId
from requests import Response
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from App.models.mongo_models import home_slider_collection, home_slider_helper, home_slider
from App.database.mongo_database import db
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from App.Services import base
ModelType = TypeVar("ModelType", bound=base.Base)


class crud_model(Generic[ModelType]):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if crud_model.__instance == None:
            crud_model()
        return crud_model.__instance

    def __init__(self, helper: Generic[ModelType], model):
        crud_model.__instance = self
        self.model = model
        self.helper = helper

    async def get(self) -> List[Type[ModelType]]:
        return [self.helper(item) async for item in self.model.find()]


# Add a new student into to the database

    async def add(self, data) -> Type[ModelType]:
        student = await self.model.insert_one(data.dict())
        new_student = await self.model.find_one({"_id": student.inserted_id})
        return self.helper(new_student)


# Retrieve a student with a matching ID


    async def get_id(self, id: str) -> dict:
        student = await self.model.find_one({"_id": ObjectId(id)})
        if student:
            return self.helper(student)


# Update a student with a matching ID


    async def update(self, id: str, data: dict):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        student = await self.model.find_one({"_id": ObjectId(id)})
        if student:
            updated_student = await self.model.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_student:
                return True
            return False


# Delete a student from the database


    async def delete(self, id: str):
        xx = await self.model.find_one({"_id": ObjectId(id)})
        student = self.helper(xx)
        print(student)
        if student:
            await self.model.delete_one({"_id": ObjectId(id)})
        return True


home_slider_crud = crud_model(
    home_slider_helper, home_slider_collection).getInstance()
