import requests
from datetime import datetime, timedelta


def get_coordinates(city):
    """
    Get latitude and longitude for a city using Open-Meteo Geocoding API.
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    location = data["results"][0]

    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "name": location["name"],
        "country": location["country"]
    }



import requests


def get_weather_data(latitude, longitude):

    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,

        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "rain_sum",
            "precipitation_hours",
            "sunshine_duration"
        ],

        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "pressure_msl",
            "cloud_cover",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m"
        ],

        "timezone": "auto"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(response.text)
        return None

    return response.json()

if __name__ == "__main__":

    city = input("Enter city: ")

    location = get_coordinates(city)

    if location is None:
        print("City not found.")
    else:
        weather = get_weather_data(
            location["latitude"],
            location["longitude"]
        )

        print(weather)
