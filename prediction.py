import joblib
import pandas as pd

# Load model and feature list
model = joblib.load("models/rainsense_rf_model.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")


def predict_rain(features):
    """
    Predict rainfall using the trained Random Forest model.
    """

    # Create DataFrame
    df = pd.DataFrame([features])

    # Add any missing columns
    for column in feature_columns:
        if column not in df.columns:
            df[column] = 0

    # Remove extra columns (if any)
    df = df[feature_columns]

    # Prediction
    prediction = model.predict(df)[0]

    # Probability
    probability = model.predict_proba(df)[0]

    return prediction, probability