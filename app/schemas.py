from pydantic import BaseModel ,EmailStr
from typing import Optional
from bson import ObjectId




class user_register(BaseModel):

    name : str
    email : EmailStr
    password : str
    is_driver : bool = False

class Login(BaseModel):

    email : str
    password: str








