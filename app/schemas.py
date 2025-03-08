from pydantic import BaseModel ,EmailStr ,StringConstraints
from typing import Optional , Any , Annotated
from bson import ObjectId
from fastapi import Form, UploadFile, File



class user_register(BaseModel):

    name : str
    email : EmailStr
    password : str
    is_driver : bool = False

class Login(BaseModel):

    email : str
    password: str


class BikerRegister:
    def __init__(
        self,
        name: Annotated[str, Form(..., min_length=2, max_length=50)],
        email: Annotated[EmailStr, Form(...)],
        password: Annotated[str, Form(...)],  
        number_plate_no: Annotated[str, Form(..., min_length=5, max_length=15)],
        is_driver: Annotated[bool, Form()] = True
    ):
        self.name = name
        self.email = email
        self.password = password
        self.number_plate_no = number_plate_no
        self.is_driver = is_driver






