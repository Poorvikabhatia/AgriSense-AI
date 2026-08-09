from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db, Base
from models import SensorReading

from thingspeak import get_latest_sensor_data
from ml_service import predict_irrigation

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AgriSense AI API",
    description="IoT and AI-based Smart Agriculture System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AgriSense AI API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/sensor-data")
def receive_sensor_data(
    temperature: float,
    humidity: float,
    soil_moisture: int,
    db: Session = Depends(get_db)
):

    reading = SensorReading(
        temperature=temperature,
        humidity=humidity,
        soil_moisture=soil_moisture
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return {
        "message": "Sensor data stored successfully",
        "data": {
            "id": reading.id,
            "temperature": reading.temperature,
            "humidity": reading.humidity,
            "soil_moisture": reading.soil_moisture,
            "timestamp": reading.timestamp
        }
    }

@app.get("/latest-sensor-data")
def latest_sensor_data():

    data = get_latest_sensor_data()

    if data is None:
        return {
            "status": "error",
            "message": "Unable to fetch sensor data from ThingSpeak"
        }

    return {
        "status": "success",
        "data": data
    }


@app.post("/fetch-and-store")
def fetch_and_store_sensor_data(
    db: Session = Depends(get_db)
):

    # ---------------------------------------------
    # 1. Fetch latest reading from ThingSpeak
    # ---------------------------------------------

    data = get_latest_sensor_data()

    if data is None:
        return {
            "status": "error",
            "message": "Unable to fetch sensor data from ThingSpeak"
        }

    # ThingSpeak entry ID
    entry_id = data["entry_id"]

    # ---------------------------------------------
    # 2. Check whether this ThingSpeak reading
    #    has already been stored
    # ---------------------------------------------

    existing_reading = (
        db.query(SensorReading)
        .filter(
            SensorReading.thingspeak_entry_id == entry_id
        )
        .first()
    )

    if existing_reading:
        return {
            "status": "success",
            "message": "This ThingSpeak reading is already stored",
            "data": {
                "id": existing_reading.id,
                "temperature": existing_reading.temperature,
                "humidity": existing_reading.humidity,
                "soil_moisture": existing_reading.soil_moisture,
                "prediction": existing_reading.prediction,
                "recommendation": existing_reading.recommendation,
                "timestamp": existing_reading.timestamp,
                "thingspeak_entry_id": existing_reading.thingspeak_entry_id
            }
        }

    # ---------------------------------------------
    # 3. Extract sensor values
    # ---------------------------------------------

    temperature = data["temperature"]
    humidity = data["humidity"]
    soil_moisture = data["soil_moisture"]

    # ---------------------------------------------
    # 4. Run ML prediction
    # ---------------------------------------------

    prediction = predict_irrigation(
        temperature,
        humidity,
        soil_moisture
    )

    # ---------------------------------------------
    # 5. Store sensor data + prediction
    # ---------------------------------------------

    reading = SensorReading(
        temperature=temperature,
        humidity=humidity,
        soil_moisture=soil_moisture,
        prediction=prediction["prediction"],
        recommendation=prediction["recommendation"],
        thingspeak_entry_id=entry_id
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    # ---------------------------------------------
    # 6. Return complete result
    # ---------------------------------------------

    return {
        "status": "success",
        "message": "New sensor reading stored successfully",

        "sensor_data": {
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": soil_moisture,
            "thingspeak_entry_id": entry_id
        },

        "irrigation_prediction": {
            "prediction": prediction["prediction"],
            "recommendation": prediction["recommendation"],
            "probability": prediction["probability"]
        },

        "database": {
            "id": reading.id,
            "timestamp": reading.timestamp
        }
    }

@app.get("/irrigation-prediction")
def irrigation_prediction():

    # Get latest reading from ThingSpeak
    data = get_latest_sensor_data()

    if data is None:
        return {
            "status": "error",
            "message": "Unable to fetch sensor data from ThingSpeak"
        }

    # Extract sensor values
    temperature = data["temperature"]
    humidity = data["humidity"]
    soil_moisture = data["soil_moisture"]

    # Send sensor data to ML model
    prediction = predict_irrigation(
        temperature,
        humidity,
        soil_moisture
    )

    return {
        "status": "success",

        "sensor_data": {
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": soil_moisture
        },

        "irrigation_prediction": {
            "prediction": prediction["prediction"],
            "recommendation": prediction["recommendation"],
            "probability": prediction["probability"]
        }
    }

@app.get("/irrigation-history")
def irrigation_history(
    db: Session = Depends(get_db)
):
    readings = (
        db.query(SensorReading)
        .order_by(SensorReading.timestamp.desc())
        .limit(10)
        .all()
    )

    return {
        "status": "success",
        "count": len(readings),
        "data": [
            {
                "id": reading.id,
                "temperature": reading.temperature,
                "humidity": reading.humidity,
                "soil_moisture": reading.soil_moisture,
                "prediction": reading.prediction,
                "recommendation": reading.recommendation,
                "timestamp": reading.timestamp
            }
            for reading in readings
        ]
    }