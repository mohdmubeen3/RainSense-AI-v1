from utils.weather_api import get_coordinates, get_weather_data

from utils.preprocessing import (
    preprocess_weather,
    extract_features,
    engineer_features,
    encode_wind_direction,
    add_rolling_features
)
from utils.preprocessing import (
    preprocess_weather,
    extract_features,
    engineer_features,
    encode_wind_direction,
    add_rolling_features,
    encode_location
)
# Get coordinates for the city
location = get_coordinates("Lucknow")

# Fetch weather data
weather = get_weather_data(
    location["latitude"],
    location["longitude"]
)

# Convert API response to DataFrames
daily, hourly = preprocess_weather(weather)

# Generate features
features = extract_features(daily, hourly)
features = engineer_features(features, daily)
features = encode_wind_direction(features)
features = add_rolling_features(features, daily, hourly)
features = encode_location(features, "Sydney")

# Print all features
print("\n===== Generated Features =====\n")

for key, value in features.items():
    print(f"{key:20}: {value}")