# ==========================================
# RainSense AI
# Flask Backend
# Part 1
# ==========================================

from flask import Flask, render_template, request
import pandas as pd
import os

# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)

# ==========================================
# Load Machine Learning Files
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "rainfall_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoders.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "weatherAUS.csv")

import joblib

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
label_encoders = joblib.load(ENCODER_PATH)

# ==========================================
# Load Dataset
# ==========================================

weather_df = pd.read_csv(DATASET_PATH)

# ==========================================
# Dropdown Values
# ==========================================

locations = sorted(
    weather_df["Location"]
    .dropna()
    .unique()
    .tolist()
)

wind_directions = sorted(
    weather_df["WindGustDir"]
    .dropna()
    .unique()
    .tolist()
)

rain_today = ["No", "Yes"]

seasons = [
    "Summer",
    "Autumn",
    "Winter",
    "Spring"
]

# ==========================================
# Home Page
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return render_template(
        "index.html",
        locations=locations,
        wind_directions=wind_directions,
        rain_today=rain_today,
        seasons=seasons
    )
# ==========================================
# Prediction Route
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ==========================================
        # Read Form Data
        # ==========================================

        location = request.form["Location"]

        min_temp = float(request.form["MinTemp"])
        max_temp = float(request.form["MaxTemp"])

        rainfall = float(request.form["Rainfall"])
        evaporation = float(request.form["Evaporation"])
        sunshine = float(request.form["Sunshine"])

        wind_gust_dir = request.form["WindGustDir"]
        wind_gust_speed = float(request.form["WindGustSpeed"])

        wind_dir_9am = request.form["WindDir9am"]
        wind_dir_3pm = request.form["WindDir3pm"]

        wind_speed_9am = float(request.form["WindSpeed9am"])
        wind_speed_3pm = float(request.form["WindSpeed3pm"])

        humidity_9am = float(request.form["Humidity9am"])
        humidity_3pm = float(request.form["Humidity3pm"])

        pressure_9am = float(request.form["Pressure9am"])
        pressure_3pm = float(request.form["Pressure3pm"])

        cloud_9am = float(request.form["Cloud9am"])
        cloud_3pm = float(request.form["Cloud3pm"])

        temp_9am = float(request.form["Temp9am"])
        temp_3pm = float(request.form["Temp3pm"])

        rain_today_value = request.form["RainToday"]

        year = int(request.form["Year"])
        month = int(request.form["Month"])
        day = int(request.form["Day"])

        season_value = request.form["Season"]

        # ==========================================
        # Encode Categorical Features
        # ==========================================

        location = label_encoders["Location"].transform([location])[0]

        wind_gust_dir = label_encoders["WindGustDir"].transform(
            [wind_gust_dir]
        )[0]

        wind_dir_9am = label_encoders["WindDir9am"].transform(
            [wind_dir_9am]
        )[0]

        wind_dir_3pm = label_encoders["WindDir3pm"].transform(
            [wind_dir_3pm]
        )[0]

        rain_today_encoded = label_encoders["RainToday"].transform(
            [rain_today_value]
        )[0]

        season_encoded = label_encoders["Season"].transform(
            [season_value]
        )[0]

        # ==========================================
        # Feature Vector
        # ==========================================

        features = [[

            location,
            min_temp,
            max_temp,
            rainfall,
            evaporation,
            sunshine,
            wind_gust_dir,
            wind_gust_speed,
            wind_dir_9am,
            wind_dir_3pm,
            wind_speed_9am,
            wind_speed_3pm,
            humidity_9am,
            humidity_3pm,
            pressure_9am,
            pressure_3pm,
            cloud_9am,
            cloud_3pm,
            temp_9am,
            temp_3pm,
            rain_today_encoded,
            year,
            month,
            day,
            season_encoded

        ]]

        feature_columns = [

            "Location",
            "MinTemp",
            "MaxTemp",
            "Rainfall",
            "Evaporation",
            "Sunshine",
            "WindGustDir",
            "WindGustSpeed",
            "WindDir9am",
            "WindDir3pm",
            "WindSpeed9am",
            "WindSpeed3pm",
            "Humidity9am",
            "Humidity3pm",
            "Pressure9am",
            "Pressure3pm",
            "Cloud9am",
            "Cloud3pm",
            "Temp9am",
            "Temp3pm",
            "RainToday",
            "Year",
            "Month",
            "Day",
            "Season"

        ]

        input_df = pd.DataFrame(
            features,
            columns=feature_columns
        )

        # ==========================================
        # Scale Input
        # ==========================================

        scaled_input = scaler.transform(input_df)

        # ==========================================
        # Prediction
        # ==========================================

        prediction = model.predict(scaled_input)[0]

        print("=" * 60)
        print("Prediction:", prediction)
        print("Prediction Type:", type(prediction))
        print("=" * 60)

        confidence = model.predict_proba(scaled_input)[0]
        confidence_percentage = round(max(confidence) * 100, 2)

        # ==========================================
        # Convert Prediction
        # ==========================================

        if prediction == 1 or prediction == "Yes":
            prediction_text = "Rain Expected Tomorrow"
        else:
            prediction_text = "No Rain Expected Tomorrow"

        # ==========================================
        # Return Result
        # ==========================================

        return render_template(

            "index.html",

            locations=locations,
            wind_directions=wind_directions,
            rain_today=["No", "Yes"],
            seasons=seasons,

            prediction=prediction_text,
            confidence=confidence_percentage

        )

    except Exception as error:

        print("ERROR:", error)

        return render_template(

            "index.html",

            locations=locations,
            wind_directions=wind_directions,
            rain_today=["No", "Yes"],
            seasons=seasons,

            prediction=f"Error: {error}",
            confidence=0

        )

# ==========================================
# Run Flask App
# ==========================================



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
