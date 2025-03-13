from datetime import datetime, timedelta,UTC
from jose import jwt, JWTError
from fastapi import Depends , HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from app.database import get_db, user_coll
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext (schemes=["bcrypt"], deprecated= "auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plan_password, hashed_pasword) -> bool:
    return pwd_context.verify(plan_password,hashed_pasword)

def create_access_token(data : dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Correct
    return encoded_jwt 

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email = payload.get("sub")
        print(email)
        role = payload.get("role")
        print(role)

        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid Token")

        return {"sub": email, "role": role}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorClient = Depends(get_db)):
    payload = decode_access_token(token= token)
    user_collection: AsyncIOMotorCollection = db["user_collection"]
    user = await user_collection.find_one({"email": payload["sub"]})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user
