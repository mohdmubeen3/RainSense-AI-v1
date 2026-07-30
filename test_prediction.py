from utils.weather_api import get_coordinates, get_weather_data

from utils.preprocessing import (
    preprocess_weather,
    extract_features,
    engineer_features,
    encode_wind_direction,
    add_rolling_features,
    encode_location
)

from prediction import predict_rain


def main():

    # ============================
    # Change city here
    # ============================
    city = "Sydney"

    print(f"\nFetching weather for {city}...\n")

    # Get coordinates
    location = get_coordinates(city)

    # Get weather data
    weather = get_weather_data(
        location["latitude"],
        location["longitude"]
    )

    # Preprocess weather data
    daily, hourly = preprocess_weather(weather)

    # Feature Engineering
    features = extract_features(daily, hourly)

    features = engineer_features(features, daily)

    features = encode_wind_direction(features)

    features = add_rolling_features(
        features,
        daily,
        hourly
    )

    features = encode_location(
        features,
        city
    )

    # Prediction
    prediction, probability = predict_rain(features)

    print("=" * 40)
    print("        RAINSENSE AI RESULT")
    print("=" * 40)

    if prediction == 1:
        print("Prediction : 🌧 Rain Tomorrow")
    else:
        print("Prediction : ☀ No Rain Tomorrow")

    print(f"\nRain Probability     : {probability[1] * 100:.2f}%")
    print(f"No Rain Probability  : {probability[0] * 100:.2f}%")

    print("=" * 40)


if __name__ == "__main__":
    main()