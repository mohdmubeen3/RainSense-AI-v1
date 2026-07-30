import pandas as pd
import numpy as np


def preprocess_weather(api_data):
    daily = pd.DataFrame(api_data["daily"])
    hourly = pd.DataFrame(api_data["hourly"])

    daily["time"] = pd.to_datetime(daily["time"])
    hourly["time"] = pd.to_datetime(hourly["time"])

    return daily, hourly


def extract_features(daily, hourly):
    """
    Extract raw weather features from Open-Meteo API.
    """

    latest_day = daily.iloc[-1]

    # Select 9 AM and 3 PM
    hour9 = hourly[hourly["time"].dt.hour == 9].iloc[-1]
    hour15 = hourly[hourly["time"].dt.hour == 15].iloc[-1]

    features = {
        "MinTemp": latest_day["temperature_2m_min"],
        "MaxTemp": latest_day["temperature_2m_max"],
        "Rainfall": latest_day["rain_sum"],
        "Sunshine": latest_day["sunshine_duration"] / 3600,  # seconds → hours

        "Temp9am": hour9["temperature_2m"],
        "Temp3pm": hour15["temperature_2m"],

        "Humidity9am": hour9["relative_humidity_2m"],
        "Humidity3pm": hour15["relative_humidity_2m"],

        "Pressure9am": hour9["pressure_msl"],
        "Pressure3pm": hour15["pressure_msl"],

        "Cloud9am": hour9["cloud_cover"],
        "Cloud3pm": hour15["cloud_cover"],

        "WindSpeed9am": hour9["wind_speed_10m"],
        "WindSpeed3pm": hour15["wind_speed_10m"],

        "WindGustSpeed": hourly["wind_gusts_10m"].max(),

        "WindDir9am": hour9["wind_direction_10m"],
        "WindDir3pm": hour15["wind_direction_10m"],

        "WindGustDir": hourly.loc[
            hourly["wind_gusts_10m"].idxmax(),
            "wind_direction_10m"
        ]
    }

    return features
def engineer_features(features, daily):
    """
    Create engineered features expected by the trained model.
    """

    latest_day = daily.iloc[-1]
    date = latest_day["time"]

    features["Year"] = date.year
    features["Month"] = date.month
    features["Day"] = date.day
    features["DayOfWeek"] = date.dayofweek

    # RainToday
    features["RainToday"] = 1 if features["Rainfall"] >= 1.0 else 0

    # Average Temperature
    features["AvgTemp"] = (
        features["MinTemp"] +
        features["MaxTemp"]
    ) / 2

    # Temperature Range
    features["TempRange"] = (
        features["MaxTemp"] -
        features["MinTemp"]
    )

    # Average Humidity
    features["AvgHumidity"] = (
        features["Humidity9am"] +
        features["Humidity3pm"]
    ) / 2

    # Average Pressure
    features["AvgPressure"] = (
        features["Pressure9am"] +
        features["Pressure3pm"]
    ) / 2

    # Pressure Change
    features["PressureChange"] = (
        features["Pressure3pm"] -
        features["Pressure9am"]
    )

    # Average Wind Speed
    features["AvgWindSpeed"] = (
        features["WindSpeed9am"] +
        features["WindSpeed3pm"]
    ) / 2

    return features
def encode_wind_direction(features):
    """
    Convert wind directions (degrees) to sin/cos representation.
    """

    import numpy as np

    def encode(angle):
        radians = np.radians(angle)
        return np.sin(radians), np.cos(radians)

    features["WindGustDir_sin"], features["WindGustDir_cos"] = encode(
        features["WindGustDir"]
    )

    features["WindDir9am_sin"], features["WindDir9am_cos"] = encode(
        features["WindDir9am"]
    )

    features["WindDir3pm_sin"], features["WindDir3pm_cos"] = encode(
        features["WindDir3pm"]
    )

    return features
def add_rolling_features(features, daily, hourly):
    """
    Compute rolling features using the weather history
    returned by the Open-Meteo API.
    """

    # ---------- Temperature ----------
    features["AvgTemp_7D"] = (
        (daily["temperature_2m_max"] + daily["temperature_2m_min"]) / 2
    ).mean()

    # ---------- Rainfall ----------
    features["Rainfall_7D"] = daily["rain_sum"].mean()

    # ---------- Humidity ----------
    humidity_daily = (
        hourly.groupby(hourly["time"].dt.date)["relative_humidity_2m"]
        .mean()
    )

    features["AvgHumidity_7D"] = humidity_daily.mean()

    # ---------- Wind Speed ----------
    wind_daily = (
        hourly.groupby(hourly["time"].dt.date)["wind_speed_10m"]
        .mean()
    )

    features["AvgWindSpeed_7D"] = wind_daily.mean()

    # ---------- Pressure ----------
    pressure_daily = (
        hourly.groupby(hourly["time"].dt.date)["pressure_msl"]
        .mean()
    )

    features["AvgPressure_7D"] = pressure_daily.mean()

    return features
def encode_location(features, city):
    """
    One-hot encode the location.
    """

    locations = [
        "Albany", "Albury", "AliceSprings", "BadgerysCreek",
        "Ballarat", "Bendigo", "Brisbane", "Cairns",
        "Canberra", "Cobar", "CoffsHarbour", "Dartmoor",
        "Darwin", "GoldCoast", "Hobart", "Katherine",
        "Launceston", "Melbourne", "MelbourneAirport",
        "Mildura", "Moree", "MountGambier", "MountGinini",
        "Newcastle", "Nhil", "NorahHead", "NorfolkIsland",
        "Nuriootpa", "PearceRAAF", "Penrith", "Perth",
        "PerthAirport", "Portland", "Richmond", "Sale",
        "SalmonGums", "Sydney", "SydneyAirport",
        "Townsville", "Tuggeranong", "Uluru",
        "WaggaWagga", "Walpole", "Watsonia",
        "Williamtown", "Witchcliffe",
        "Wollongong", "Woomera"
    ]

    # Initialize all location columns to 0
    for location in locations:
        features[f"Location_{location}"] = 0

    # Set the selected location to 1 if it exists
    if city in locations:
        features[f"Location_{city}"] = 1
    else:
        print(f"Warning: '{city}' is not in the training locations.")

    return features