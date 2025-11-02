from typing import Optional
from datetime import datetime
from uuid import uuid4
from copy import deepcopy

from app.domain.model.weather_data import WeatherData
from app.persistance.repositories.measurement_repository import WeatherMeasurementRepository


class InMemoryWeatherMeasurementRepository(WeatherMeasurementRepository):

    def __init__(self):
        self._data: list[WeatherData] = []

    def get_chart_data(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        sort_by: Optional[list[str]] = None,
    ) -> tuple[list[WeatherData], int]:
        results = self._data
        if start_date:
            results = [m for m in results if m.time >= start_date]
        if end_date:
            results = [m for m in results if m.time <= end_date]

        if sort_by:
            for item in reversed(sort_by):
                field, _, direction = item.partition(":")
                reverse = direction.lower() == "desc"

                results.sort(
                    key=lambda x: getattr(x, field, None) if getattr(x, field, None) is not None else float('-inf'),
                    reverse=reverse
                )

        return deepcopy(results), len(results)

    def get_by_id(self, weather_id: str) -> Optional[WeatherData]:
        for m in self._data:
            if m.id == weather_id:
                return deepcopy(m)
        return None

    def add(self, measurement: WeatherData) -> WeatherData:
        if not measurement.id:
            measurement.id = str(uuid4())

        if not self._data.__contains__(measurement):
            self._data.append(deepcopy(measurement))
        return deepcopy(measurement)

    def measurement_exists(self, city: str, timestamp: datetime) -> bool:
        for measurement in self._data:
            if measurement.city == city and measurement.time == timestamp:
                return True
        return False
