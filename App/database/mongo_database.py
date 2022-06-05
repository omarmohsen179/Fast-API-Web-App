import motor.motor_asyncio
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Body, HTTPException, status
import os
from pymongo import MongoClient
#client = MongoClient("mongodb+srv://ecom_app:1eFuHfWrbg7U0XnT@cluster0.mmwzwf2.mongodb.net/?retryWrites=true&w=majority")
#db = client.test

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://ecom_app:1eFuHfWrbg7U0XnT@cluster0.mmwzwf2.mongodb.net/?retryWrites=true&w=majority")
db = client.Ecommerce


class PyObjectId(ObjectId):
    """ Custom Type for reading MongoDB IDs """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Student(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str
    last_name: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
