from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"

locations = json.load(open('cities.json'))

def get_city_coordinates(location_name, api_key):
    """GET the latitude and longitude of a city."""
    params = {
        "q": location_name,
        "appid": api_key,
        "limit": 1
    }
    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        print(f"Could not find coordinates for {location_name}")
        return None, None

def get_weather(lat, lon, api_key):
    """GET the current weather data using latitude and longitude."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def main():
    for location in locations:
        location_name = f"{location['city']},{location['country']}"

        lat, lon = get_city_coordinates(location_name, API_KEY)
        if lat is not None and lon is not None:
            weather_data = get_weather(lat, lon, API_KEY)
            print(f"Weather in {location_name[:-3]}: {weather_data['weather'][0]['description']}, "
                  f"Temperature: {weather_data['main']['temp']}°C")

if __name__ == "__main__":
    main()

