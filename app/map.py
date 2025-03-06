# import requests

# def get_address_from_coordinates(latitude, longitude):
#     url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    
#     try:
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         response.raise_for_status()  # Raises an error for HTTP issues
#         data = response.json()

#         return data.get("display_name", "Address not found")
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"



import requests

def get_address_from_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/serarch"
    params = {"q": address , "formet" : "json"}
    try:
        response = requests.get(url, params= params ,headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  
        data = response.json()
    
        if data:
            latitude = data[0] ["lat"]
            longitude = data[0] ["lat"]
            return (latitude,longitude)
        else:
            return "locatin not found"
        
    except requests.exceptions.RequestException as e:
                return f"Error: {e}"