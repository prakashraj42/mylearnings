from pydantic import BaseModel ,EmailStr
from typing import Optional
from bson import ObjectId

# class PyObjectId(str):
    
#     def __get_validators__(cls):
#         yield cls.validate

#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("invalid objecid")
#         return str(v)

class UserCreate(BaseModel):

    name : str
    email : EmailStr
    password : str
    is_driver : bool = False

# class UserResponse(BaseModel):
    
#     id : PyObjectId
#     name : str
#     email : str
#     is_driver : bool


#     class config:
#         orm_mode = True
#         json_encoder = {ObjectId: str}



class BookingCreatation(BaseModel):

    pick_uplocation : str
    drop_location : str
    fare : float

# class BookingResponse(BaseModel):

#     id : PyObjectId
#     user_id : PyObjectId
#     driver_id : Optional[PyObjectId] = None 
#     pickup_location : str
#     drop_location : str
#     fare : str
#     status : str

#     class config:
#         orm_mode = True
#         json_encoder = {ObjectId : str}


