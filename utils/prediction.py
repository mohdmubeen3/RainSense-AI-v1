import os
import joblib
import pandas as pd

# ==========================================
# Load Model
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "rainsense_rf_model.pkl"
)

FEATURE_COLUMNS_PATH = os.path.join(
    BASE_DIR,
    "model",
    "feature_columns.pkl"
)

model = joblib.load(MODEL_PATH)

feature_columns = joblib.load(FEATURE_COLUMNS_PATH)


# ==========================================
# Prediction Function
# ==========================================

def predict_rain(features):
    """
    Predict tomorrow's rainfall.

    Parameters
    ----------
    features : dict
        Engineered feature dictionary.

    Returns
    -------
    prediction : int
        0 = No Rain
        1 = Rain

    probability : ndarray
        [No Rain Probability, Rain Probability]
    """

    # Convert dictionary to DataFrame

    df = pd.DataFrame([features])

    # Add any missing columns

    for column in feature_columns:

        if column not in df.columns:

            df[column] = 0

    # Keep only model columns

    df = df[feature_columns]

    # Prediction

    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0]

    return prediction, probability


# ==========================================
# Local Testing
# ==========================================

if __name__ == "__main__":

    print("=" * 50)

    print("RainSense AI Prediction Module Loaded Successfully")

    print("=" * 50)

    print("Expected Features :", len(feature_columns))

    print("Model Loaded :", type(model).__name__)