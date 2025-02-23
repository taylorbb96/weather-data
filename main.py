import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"

# TODO: Import cities and country codes from json file
cities = [
    "New York City", "London", "Tokyo", "Sydney", "Berlin"
]

def get_city_coordinates(city_name, api_key):
    """Fetches the latitude and longitude of a city."""
    params = {
        "q": city_name,
        "appid": api_key,
        "limit": 1
    }
    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        print(f"Could not find coordinates for {city_name}")
        return None, None

def get_weather(lat, lon, api_key):
    """Fetches the current weather data using latitude and longitude."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def main():
    for city in cities:
        lat, lon = get_city_coordinates(city, API_KEY)
        if lat is not None and lon is not None:
            weather_data = get_weather(lat, lon, API_KEY)
            print(f"Weather in {city}: {weather_data['weather'][0]['description']}, "
                  f"Temperature: {weather_data['main']['temp']}°C")

if __name__ == "__main__":
    main()

