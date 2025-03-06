from fastapi import APIRouter, FastAPI
from  app.schemas import user_register, Login
from app.service import resgitration, login
from typing import Optional


router = APIRouter()

@router.post("/register")
async def register(user: user_register):
    return await resgitration(user)

@router.post("/user")
async def user_login(request: Login, user_type : Optional[bool] =False ):
    return await login(login= request, user_type= user_type )