from motor.motor_asyncio  import AsyncIOMotorClient
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_URL = "MONGO_URI"
DB_NAME = "bike booking"

client = AsyncIOMotorClient(MONGO_URL)
db = client(DB_NAME)



