from datetime import datetime, timedelta,UTC
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
load_dotenv()

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

def decode_access_token(token: str) -> dict:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None




# def run():
#     password = "my_secure_password"
#     hashed_password = hash_password(password)
#     print("Hashed Password:", hashed_password)

#     is_valid = verify_password(password, hashed_password)
#     print("Password Valid:", is_valid)

#     token_data = {"sub": "user123"}  # Example payload
#     token = create_access_token(token_data)
#     print("Generated Token:", token)

#     decoded_data = decode_access_token(token)
#     print("Decoded Token Data:", decoded_data)

# # Run the function
# run()

