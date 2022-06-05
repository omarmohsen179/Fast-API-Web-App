from typing import List, Optional, Any
from datetime import date, datetime, timedelta
from numpy import integer
from pydantic import Field, validator, BaseModel, EmailStr
from App.database.mongo_database import PyObjectId, db

from bson import ObjectId


def home_slider_helper(student) -> dict:
    return {
        "Id": str(student["_id"]),
        "image_path": student["image_path"],
        "item_id": student["item_id"],
    }


class home_slider(BaseModel):
    Id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    image_path: str = Field(...)
    item_id: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


home_slider_collection = db.get_collection("home_slider_collection")
