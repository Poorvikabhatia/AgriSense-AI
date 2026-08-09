import joblib
import pandas as pd
from pathlib import Path


# Path to trained ML model
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml"
    / "irrigation_model.pkl"
)


# Load model once when FastAPI starts
model = joblib.load(MODEL_PATH)


def predict_irrigation(
    temperature: float,
    humidity: float,
    soil_moisture: int
):
    # Create input DataFrame
    input_data = pd.DataFrame([
        {
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": soil_moisture
        }
    ])

    # Prediction
    prediction = int(model.predict(input_data)[0])

    # Prediction probability
    probabilities = model.predict_proba(input_data)[0]

    if prediction == 1:
        recommendation = "Water Needed"
    else:
        recommendation = "No Water Needed"

    return {
        "prediction": prediction,
        "recommendation": recommendation,
        "probability": round(float(probabilities[prediction]), 4)
    }