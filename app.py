from flask import Flask, render_template, request

from utils.weather_api import get_coordinates, get_weather_data

from utils.preprocessing import (
    preprocess_weather,
    extract_features,
    engineer_features,
    encode_wind_direction,
    add_rolling_features,
    encode_location,
)

from prediction import predict_rain

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:

        city = request.form["city"].strip()

        if city == "":
            return render_template(
                "index.html",
                error="Please enter a city name."
            )

        # -----------------------------
        # Get Coordinates
        # -----------------------------

        location = get_coordinates(city)

        if location is None:

            return render_template(
                "index.html",
                error="City not found."
            )

        # -----------------------------
        # Get Weather Data
        # -----------------------------

        api_data = get_weather_data(
            location["latitude"],
            location["longitude"]
        )

        if api_data is None:

            return render_template(
                "index.html",
                error="Unable to fetch weather information."
            )

        # -----------------------------
        # Preprocessing
        # -----------------------------

        daily, hourly = preprocess_weather(api_data)

        features = extract_features(
            daily,
            hourly
        )

        features = engineer_features(
            features,
            daily
        )

        features = encode_wind_direction(
            features
        )

        features = add_rolling_features(
            features,
            daily,
            hourly
        )

        features = encode_location(
            features,
            location["name"]
        )

        # -----------------------------
        # Prediction
        # -----------------------------

        prediction, probability = predict_rain(features)

        prediction_text = (
            "🌧 Rain Tomorrow"
            if prediction == 1
            else "☀ No Rain Tomorrow"
        )

        weather_summary = {

            "temperature": round(
                features["AvgTemp"],
                1
            ),

            "humidity": round(
                features["AvgHumidity"],
                1
            ),

            "wind_speed": round(
                features["AvgWindSpeed"],
                1
            ),

            "rainfall": round(
                features["Rainfall"],
                1
            ),

            "sunshine": round(
                features["Sunshine"],
                1
            )

        }

        return render_template(

            "index.html",

            city=location["name"],

            country=location["country"],

            weather=weather_summary,

            prediction=prediction_text,

            rain_probability=round(
                probability[1] * 100,
                2
            ),

            no_rain_probability=round(
                probability[0] * 100,
                2
            )

        )

    except Exception as e:

        return render_template(

            "index.html",

            error=str(e)

        )


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )