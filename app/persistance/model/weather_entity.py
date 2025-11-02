import os

from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class WeatherEntity(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, default="Warsaw")
    latitude = Column(Float, default=52.21367)
    longitude = Column(Float, default=21.005188)
    time = Column(DateTime)
    temperature_2m = Column(Float)
    temperature_2m_unit = Column(String)
    is_day = Column(Integer)
    rain = Column(Float)
    rain_unit = Column(String)
    surface_pressure = Column(Float)
    surface_pressure_unit = Column(String)
    wind_speed_10m = Column(Float)
    wind_speed_10m_unit = Column(String)
