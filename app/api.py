from fastapi import APIRouter, Depends, HTTPException
from app import schemas, database
from bson import ObjectId
import bcrypt


router = APIRouter()
#Add new user
@router.post("/user/", response_model=schemas.UserResponse)
async def Create_user(user : schemas.UserCreate):
    
    existing_user = await database.db.users.find_one({"email" : user.email})
    if existing_user:
        raise HTTPException (status_code=400, detail= "Email id already exist")


    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    new_user ={
        "name"  : user.name,
        "mail"  : user.email,
        "hashed_password" : hashed_password.encode("utf-8"),
        "is_driver" : user.is_driver
    } 

    result = await database.db.users.insert_one(new_user)
    return {**new_user, "id" :str (result.insered_id)}


#booking bike
@router.post("/bookings/" ,response_model= schemas.BookingResponse)
async def Create_booking(booking : schemas.BookingCreatation, user_id :str):

    new_booking = {

        "user_id" : ObjectId(user_id),
        "driver_id" : None,
        "pickup_location" : booking.pick_uplocation,
        "drop_location" : booking.drop_location,
        "fare" : booking.fare,
        "status": booking.status
    }

    result =  await database.db.booking.insert_one(new_booking)
    return {**new_booking, "id":str (result.inserted_id)}


