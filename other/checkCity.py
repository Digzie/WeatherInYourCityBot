import requests
def CheckCity(lat:float, lon:float):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {
            'User-Agent': 'WeatherBot (sdaw23@email.com)'  
        }
    response = requests.get(url, headers=headers).json()
    city = response['address']['city']
    return city

