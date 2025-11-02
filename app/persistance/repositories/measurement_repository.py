from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.domain.model.weather_data import WeatherData


class WeatherMeasurementRepository(ABC):
    @abstractmethod
    def get_chart_data(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        sort_by: Optional[list[str]] = None,
    ) -> tuple[list[WeatherData], int]:
        pass


    @abstractmethod
    def get_by_id(self, weather_id: str) -> Optional[WeatherData]:
        pass

    @abstractmethod
    def add(self, measurement: WeatherData) -> WeatherData:
        pass

    @abstractmethod
    def measurement_exists(self, city: str, timestamp: datetime) -> bool:
        pass
