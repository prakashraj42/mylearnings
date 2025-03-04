from fastapi import APIRouter, Depends, HTTPException
from app import schemas, database
from app.database import get_db, user_coll, booking_coll
from bson import ObjectId
import bcrypt


router = APIRouter()
#Add new user
@router.post("/user/")
async def Create_user(user : schemas.UserCreate):

    # existing_user =  user_coll.find_one({"email" : user.email})
    # if existing_user:
    #     raise HTTPException (status_code=400, detail= "Email id already exist")


    # hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    new_user ={
        "name"  : user.name,
        "email"  : user.email,
        "hashed_password" : user.password,
        "is_driver" : user.is_driver
    } 

    result = user_coll.insert_one(new_user)
    return {"Done"}


#booking bike
@router.post("/bookings/" )
async def Create_booking(booking : schemas.BookingCreatation, user_id :str):

    new_booking = {

        "user_id" : ObjectId(user_id),
        "driver_id" : None,
        "pickup_location" : booking.pick_uplocation,
        "drop_location" : booking.drop_location,
        "fare" : booking.fare,
        "status": booking.status
    }

    result =  booking_coll.insert_one(new_booking)
    return {**new_booking, "id":str (result.inserted_id)}


