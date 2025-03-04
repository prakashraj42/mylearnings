from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv (int("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext  (schemes=["bcrypt"], depricate = "auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plan_password, hashed_pasword) -> bool:
    return pwd_context.verify(plan_password,hashed_pasword)

def create_access_token(data : dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.expire({"exp": expire})

def decode_access_token(token: str) -> dict:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

    




