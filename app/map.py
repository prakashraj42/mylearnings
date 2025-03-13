import requests
from math import radians, sin, cos, sqrt, atan2
from app.database import user_booking_info_coll
from bson import ObjectId


async def get_address_from_coordinates(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    
    try:
        response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  
        data = response.json()


        if data:
            return {
                "name": data[0].get("name", "N/A"),
                "display_name": data[0].get("display_name", "N/A"),
                "latitude": float(data[0]["lat"]),   # Convert to float
                "longitude": float(data[0]["lon"])   # Convert to float
            }
        
        else:
            return None  # Return None instead of a string

    except requests.exceptions.RequestException as e:
        return None  # Return None if an error occurs


async def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c  # Distance in km


from bson import ObjectId
from fastapi.encoders import jsonable_encoder

async def get_distance_between_locations(start_address, destination_address):
    
    start_coord = await get_address_from_coordinates(start_address)
    destination_coord = await get_address_from_coordinates(destination_address)

    if start_coord and destination_coord:
        distance = await haversine_distance(
            start_coord["latitude"], start_coord["longitude"],
            destination_coord["latitude"], destination_coord["longitude"]
        )

        total_fare = await km_fare(distance)

        booking_data = {
            "start_location": start_address,
            "destination_location": destination_address,
            "start_coordinates": {
                "latitude": start_coord["latitude"],
                "longitude": start_coord["longitude"]
            },
            "destination_coordinates": {
                "latitude": destination_coord["latitude"],
                "longitude": destination_coord["longitude"]
            },
            "distance_km": round(distance, 2),
            "total_fare": total_fare,
            "status": "pending",
            "biker_id" : "biker"
            
        }

        inserted_booking = await user_booking_info_coll.insert_one(booking_data)

        booking_data["_id"] = str(inserted_booking.inserted_id)

        return jsonable_encoder(booking_data)  

    else:
        return {"error": "Could not find coordinates for one or both locations."}


async def km_fare(distance):

    Per_km_fare = 10
    Booking_fare = round(distance * Per_km_fare,2)
    return Booking_fare


async def biker_location(starting_address):
        start_coord = await get_address_from_coordinates(starting_address)
        return(start_coord)





