from pydantic import BaseModel ,EmailStr
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class UserCreate(BaseModel):

    id: Optional[PyObjectId] = None
    name : str
    email : EmailStr
    password : str
    is_driver : bool = False


class BookingCreatation(BaseModel):
     
    id: Optional[PyObjectId] = None
    user_id: str
    pick_uplocation : str
    drop_location : str
    fare : float




