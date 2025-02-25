from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

# TODO: Validate this works, key is being activated
# Also test non-overview endpoint
GEOCODE_API_KEY = os.getenv("OPENWEATHER_GEOCODE_API_KEY")
ONE_CALL_API_KEY = os.getenv("OPENWEATHER_ONE_CALL_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall/overview"
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
    results = []

    with open('results.json', 'w', encoding='utf-8') as output_file:
        for location in locations:
            location_name = f"{location['city']},{location['country']}"

            lat, lon = get_city_coordinates(location_name, GEOCODE_API_KEY)

            if lat is not None and lon is not None:
                weather_data = get_weather(lat, lon, ONE_CALL_API_KEY)
                results.append(weather_data)

        json.dump(results, output_file)

if __name__ == "__main__":
    main()

