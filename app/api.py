from fastapi import APIRouter, Depends, HTTPException
from app import schemas, database
from app.database import get_db, user_coll, booking_coll
from bson import ObjectId
import bcrypt
from app.auth import decode_access_token


router = APIRouter()


def get_current_user(token : str):

    payload = decode_access_token(token)
    if not  payload:
        raise HTTPException(status_code=401, detail= "invalid token")
    return payload["user_id"]


#Add new user
@router.post("/user/")
async def user_registration(user : schemas.UserCreate):


    existing_user = user_coll.find_one({"email" : user.email})
    if  existing_user:
        raise HTTPException(status_code=400 ,detail= "Email already registered")


    new_user ={
        "name"  : user.name,
        "email"  : user.email,
        "hashed_password" : user.password,
        "is_driver" : user.is_driver
    } 

    result = user_coll.insert_one(new_user)
    return {"message" : "user registerd successfully", "id" : str(result.inserted_id)}







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


