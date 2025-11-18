import os

from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    print("DATABASE_URL is missing! Fallback to SQLite.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
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

    def __str__(self) -> str:
        day_status = "Day" if self.is_day else "Night"
        return (
            f"WeatherData(id={self.id}, city={self.city}, time={self.time.isoformat()}, "
            f"temperature={self.temperature}{self.temperature_unit}, "
            f"{day_status}, rain={self.rain}{self.rain_unit}, "
            f"surface_pressure={self.surface_pressure}{self.surface_pressure_unit}, "
            f"wind_speed={self.wind_speed}{self.wind_speed_unit})"
        )

def init_db():
    Base.metadata.create_all(bind=engine)
