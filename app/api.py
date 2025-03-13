from fastapi import APIRouter, FastAPI , Response, UploadFile, File, Depends
from  app.schemas import user_register, Login, BikerRegister
from app.service import user_resgitration, login, get_users, get_bikers,biker_resgitration, biker_get_bookings, assign_biker, confirm_booking
from typing import Optional 
from app.map import get_address_from_coordinates, get_distance_between_locations, biker_location
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()




@router.post("/user_register/",tags=["Authentication"])
async def user_registering(user: user_register):
    
    return await user_resgitration(user)


@router.post("/biker_register/",tags=["Authentication"])
async def biker_registering(biker: BikerRegister = Depends(),license: UploadFile = File(...)):
    return await biker_resgitration(biker,license)

@router.post("/user/", tags=["Authentication"])
async def user_login(request: Login, responses: Response, user_type : Optional[bool] =False):
    return await login(login= request, user_type= user_type , responses= responses )

@router.get("/users/", tags=["users"])
async def get_user():
    return await get_users()

@router.get("/bikers/", tags=["bikers"])
async def get_biker(token: dict = Depends(decode_access_token)):
    return await get_bikers(token)

@router.post("/Bike_Booking/", tags=["users"])
async def get_user_location(start, destination):
    
    return await get_distance_between_locations(start_address= start, destination_address= destination)

@router.get("/get_biker_location/", tags=["bikers"])
async def get_biker_location(matching_bookings):
    return await biker_get_bookings(matching_bookings)


# @router.post("/Approve_booking/")
# async def approve_booking(booking_id: str):
#     return  {"booking_id": booking_id , "message": "Booking approved and details sent to both user and biker."}

@router.post("/assign_biker/", tags=["users"])
async def check(booking_id, biker_id):
  return await assign_biker(booking_id, biker_id, res)


@router.post("/biker/confirm_booking/", tags=["bikers"])
async def approve(booking_id: str):
    return await confirm_booking(booking_id)
