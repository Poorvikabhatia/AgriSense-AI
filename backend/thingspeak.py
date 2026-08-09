import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# THINGSPEAK CONFIGURATION
# ==========================================

CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID")
READ_API_KEY = os.getenv("THINGSPEAK_READ_API_KEY")

THINGSPEAK_URL = (
    f"https://api.thingspeak.com/channels/"
    f"{CHANNEL_ID}/feeds/last.json"
)


# ==========================================
# GET LATEST SENSOR DATA
# ==========================================

def get_latest_sensor_data():

    params = {
        "api_key": READ_API_KEY
    }

    try:

        response = requests.get(
            THINGSPEAK_URL,
            params=params,
            timeout=10
        )

        # Raise an error if ThingSpeak returns
        # something other than a successful response
        response.raise_for_status()

        data = response.json()

        # Convert ThingSpeak field values to numbers
        sensor_data = {
            "temperature": float(data["field1"]),
            "humidity": float(data["field2"]),
            "soil_moisture": int(float(data["field3"])),
            "entry_id": data["entry_id"],
            "created_at": data["created_at"]
        }

        return sensor_data

    except requests.exceptions.RequestException as e:

        print("ThingSpeak connection error:", e)
        return None

    except (KeyError, TypeError, ValueError) as e:

        print("Invalid ThingSpeak data:", e)
        return None