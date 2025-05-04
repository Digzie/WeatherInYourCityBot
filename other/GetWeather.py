import requests
API_WEATHER = "" #https://home.openweathermap.org/api_keys
def Weather(city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric"
    response = requests.get(url).json()

    return {
        "temp": response["main"]["temp"],
        "like": response["main"]["feels_like"],
        "weather": response["weather"][0]["main"].lower(),
        "wind": response["wind"]["speed"]
    }
