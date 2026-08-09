from sqlalchemy import Column, Integer, Float, String, DateTime, String
from datetime import datetime

from database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)

    temperature = Column(Float, nullable=False)

    humidity = Column(Float, nullable=False)

    soil_moisture = Column(Integer, nullable=False)

    prediction = Column(Integer, nullable=True)

    recommendation = Column(String, nullable=True)

    thingspeak_entry_id = Column(
        Integer,
        unique=True,
        nullable=True,
        index=True
    )

    timestamp = Column(DateTime, default=datetime.utcnow)