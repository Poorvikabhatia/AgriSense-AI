from backend.thingspeak import get_latest_sensor_data

data = get_latest_sensor_data()

print("Latest Sensor Data:")
print(data)