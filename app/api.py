from fastapi import APIRouter, FastAPI , Response
from  app.schemas import user_register, Login
from app.service import resgitration, login, get_users, get_bikers
from typing import Optional
from app.map import get_address_from_coordinates

router = APIRouter()

@router.post("/register")
async def register(user: user_register):
    return await resgitration(user)

@router.post("/user/")
async def user_login(request: Login, responses: Response, user_type : Optional[bool] =False):
    return await login(login= request, user_type= user_type , responses= responses)

@router.get("/users/")
async def get_user():
    return await get_users()

@router.get("/bikers/")
async def get_biker():
    return await get_bikers()

@router.get("/get-location/")
async def get_user_location(address):
    return await get_address_from_coordinates(address)