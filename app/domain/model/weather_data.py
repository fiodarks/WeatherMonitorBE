from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class WeatherData(BaseModel):
    id: Optional[str] = None
    city: str
    time: datetime
    temperature: float
    temperature_unit: str
    is_day: bool
    rain: float
    rain_unit: str
    surface_pressure: float
    surface_pressure_unit: str
    wind_speed: float
    wind_speed_unit: str

    def __str__(self) -> str:
        day_status = "Day" if self.is_day else "Night"
        return (
            f"WeatherData(id={self.id}, city={self.city}, time={self.time.isoformat()}, "
            f"temperature={self.temperature}{self.temperature_unit}, "
            f"{day_status}, rain={self.rain}{self.rain_unit}, "
            f"surface_pressure={self.surface_pressure}{self.surface_pressure_unit}, "
            f"wind_speed={self.wind_speed}{self.wind_speed_unit})"
        )