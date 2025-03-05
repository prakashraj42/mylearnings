from motor.motor_asyncio  import AsyncIOMotorClient
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_URL = os.getenv("MONGO_URI")

DB_NAME = "bike_booking"

client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client[DB_NAME]


user_coll = db["user_collection"]
biker_coll = db["biker_collection"]
booking_coll = db["booking_collection"]
async def get_db():
    yield db


