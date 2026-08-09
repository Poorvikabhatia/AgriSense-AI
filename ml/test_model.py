import joblib
import pandas as pd

# Load trained model
model = joblib.load("irrigation_model.pkl")

print("Model loaded successfully!")


# Test sample
sample = pd.DataFrame([
    {
        "temperature": 30.0,
        "humidity": 50.0,
        "soil_moisture": 980
    }
])

# Make prediction
prediction = model.predict(sample)[0]

# Get probability
probability = model.predict_proba(sample)[0]

print("\nSensor Input:")
print(sample)

print("\nPrediction:")

if prediction == 1:
    print("💧 Water Needed")
else:
    print("🌱 No Water Needed")

print("\nPrediction Probability:")
print(probability)