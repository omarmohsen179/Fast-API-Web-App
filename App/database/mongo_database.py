import motor.motor_asyncio
from bson import ObjectId
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://ecom_app:1eFuHfWrbg7U0XnT@cluster0.mmwzwf2.mongodb.net/?retryWrites=true&w=majority")
db = client.Ecommerce


class PyObjectId(ObjectId):

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
