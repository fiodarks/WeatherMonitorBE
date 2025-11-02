import datetime

from app.domain.model.weather_data import WeatherData
from app.persistance.model.weather_entity import WeatherEntity
from datetime import datetime
from typing import List, Optional
import requests


class OpenMeteoWeatherService:

    BASE_URL = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=52.220574159197184"
        "&longitude=21.0103649236951"
        "&current=temperature_2m,is_day,showers,rain,snowfall,surface_pressure,wind_speed_10m"
    )

    def __init__(self, measurement_repo):
        self.measurement_repo = measurement_repo

    def get_latest_measurement(self, city: str = "Warsaw") -> Optional[WeatherData]:
        response = requests.get(self.BASE_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})
        units = data.get("current_units", {})

        measurement = WeatherData(
            id="",
            city=city,
            time=datetime.fromisoformat(current["time"]),
            temperature=current.get("temperature_2m"),
            temperature_unit=units.get("temperature_2m", "°C"),
            is_day=bool(current.get("is_day", 0)),
            rain=current.get("rain", 0.0),
            rain_unit=units.get("rain", "mm"),
            surface_pressure=current.get("surface_pressure", 0.0),
            surface_pressure_unit=units.get("surface_pressure", "hPa"),
            wind_speed=current.get("wind_speed_10m", 0.0),
            wind_speed_unit=units.get("wind_speed_10m", "km/h")
        )

        if self.measurement_repo.measurement_exists(city, measurement.time):
            return None

        saved_measurement = self.measurement_repo.add(measurement)
        return saved_measurement

