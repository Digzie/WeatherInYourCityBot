import requests
import os
from dotenv import load_dotenv
load_dotenv()
API = os.getenv("OPENWEATHERMAP")
API_WEATHER = API

def Weather(city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric"
    response = requests.get(url).json()

    return {
        "temp": response["main"]["temp"],
        "like": response["main"]["feels_like"],
        "weather": response["weather"][0]["main"].lower(),
        "wind": response["wind"]["speed"]
    }
