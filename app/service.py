from fastapi import FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import user_register,Login
from app. database import db, user_coll, biker_coll 
from app.auth import create_access_token
from bson import ObjectId
from app.map import get_address_from_coordinates

async def resgitration(user : user_register):
    

    collection = biker_coll if user.is_driver else user_coll




    existing_entry = await collection.find_one({"email": user.email})

    if existing_entry:
        raise HTTPException(status_code=400, detail="Email ID already exists in this role")
    
    user_data = user.model_dump()

 
    inserter_id= await collection.insert_one(user_data)  


    return{"message" : "register successfully", "role" : "biker" if user.is_driver else "user", "inserterd_id": str(ObjectId(inserter_id.inserted_id))} #"token" : token 


async def login(login: Login, user_type : bool , responses: Response): 
    
    token_data = {"sub" : login.email , "role" : "biker" if user_type else "user"}  
    
    token = create_access_token(token_data)

    responses.headers["Authorization"] = f"Bearer {token}"

    
    if user_type == False:
        user = await user_coll.find_one({"email" : login.email})
        if not user:
            raise HTTPException(status_code=400, detail="Account not found")
        return HTTPException (status_code= 200 , detail="user login successfully")

    else:
        biker = await biker_coll.find_one({"email": login.email})
        if not biker:
            raise HTTPException(status_code= 400, detail="Account not found")
        return HTTPException (status_code= 200 , detail="Biker login successfully")


def serialize_document(doc):
    return {**doc, "_id": str(doc["_id"])} if doc else None

async def get_users():

    user =  await user_coll.find().to_list(length = None)
    if not user:
        raise HTTPException(status_code= 400, detail= "users not found")
    return [serialize_document(user) for user in user]

async def get_bikers():

    biker = await biker_coll.find().to_list(length = None)
    if not biker:
        raise HTTPException(status_code= 400, detail= "bikers not found")
    return [serialize_document(biker) for biker in biker]
    



    

    
        

    
        


