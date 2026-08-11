# AgriSense AI

An IoT and Machine Learning-based smart irrigation prediction system that monitors environmental conditions and predicts whether water is needed.

## Overview

AgriSense AI collects temperature, humidity, and soil moisture data using an ESP8266-based system. The data is transmitted to ThingSpeak, processed through a FastAPI backend, and evaluated using a machine learning model.

The prediction and sensor data are stored in SQLite and displayed through a web dashboard.

The current system focuses on **water-needed prediction** and does not directly control a physical water pump.

## Features

- Real-time temperature, humidity, and soil moisture monitoring
- ThingSpeak IoT integration
- Machine learning-based irrigation prediction
- Prediction confidence display
- SQLite-based irrigation history
- Temperature, humidity, and soil moisture trend charts
- Web-based monitoring dashboard
- REST API using FastAPI

## System Architecture

```text
ESP8266 Sensors
      |
      v
  ThingSpeak
      |
      v
 FastAPI Backend
      |
      +----------------+
      |                |
      v                v
Machine Learning    SQLite
      |                |
      +-------+--------+
              |
              v
        Web Dashboard
```

## Technology Stack

| Category | Technologies |
|---|---|
| Hardware | ESP8266, Temperature/Humidity Sensor, Soil Moisture Sensor |
| IoT | ThingSpeak |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | SQLite |
| Machine Learning | Python, Pandas, Scikit-learn |
| Frontend | HTML, CSS, JavaScript, Chart.js |

## Machine Learning

### Input Features

- Temperature
- Humidity
- Soil Moisture

### Output

```text
0 → No Water Needed
1 → Water Needed
```

## Project Structure

```text
AgriSense-AI/
│
├── backend/
│   ├── database.py
│   ├── main.py
│   ├── ml_service.py
│   ├── models.py
│   ├── requirements.txt
│   └── thingspeak.py
│
├── firmware/
│   └── agrisense.ino
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── ml/
│   ├── dataset/
│   │   └── irrigation_dataset.csv
│   ├── create_dataset.py
│   ├── irrigation_model.pkl
│   ├── test_model.py
│   └── train_model.py
│
├── .env.example
├── .gitignore
├── test_thingspeak.py
└── README.md
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Poorvikabhatia/AgriSense-AI.git
cd AgriSense-AI
```

### 2. Create Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r backend/requirements.txt
```

### 4. Configure ThingSpeak

Create a `.env` file in the project root:

```env
THINGSPEAK_CHANNEL_ID=your_channel_id
THINGSPEAK_READ_API_KEY=your_read_api_key
```

Do not commit the `.env` file to GitHub.

### 5. Start Backend

```powershell
cd backend
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start Frontend

Open `frontend/index.html` using VS Code Live Server while the FastAPI backend is running.

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | API status |
| `/health` | GET | Health check |
| `/latest-sensor-data` | GET | Latest ThingSpeak reading |
| `/fetch-and-store` | POST | Fetch, predict, and store data |
| `/irrigation-prediction` | GET | Generate irrigation prediction |
| `/irrigation-history` | GET | Retrieve prediction history |

## Current Status

The complete prototype has been tested with live ESP8266 sensor data and successfully demonstrates:

**Sensor Data → ThingSpeak → FastAPI → ML Prediction → SQLite → Web Dashboard**

## Demo Video

[Watch the AgriSense AI Project Demo](https://drive.google.com/file/d/1LgVES35Y2tuZBw9sUq2GrcNd7W2DsMbE/view?usp=sharing)

## Future Scope

- Automatic pump control using a relay
- Crop-specific irrigation recommendations
- Weather data integration
- Larger real-world agricultural datasets
- Cloud deployment
- Mobile application

## Author

**Poorvika Bhatia** - Team Zentrix

GitHub: https://github.com/Poorvikabhatia

LinkedIn: https://www.linkedin.com/in/poorvika-bhatia-45019a295/

## License

This project is intended for educational and academic purposes.
