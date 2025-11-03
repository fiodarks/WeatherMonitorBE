from app.domain.mapper import to_weather_entity, to_weather_data
from app.domain.model.weather_data import WeatherData
from app.persistance.model.weather_entity import WeatherEntity
from app.persistance.repositories.measurement_repository import WeatherMeasurementRepository

from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from datetime import datetime

class SQLMeasurementRepository(WeatherMeasurementRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, measurement: WeatherData) -> WeatherData:
        db_obj = to_weather_entity(measurement)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return to_weather_data(db_obj)

    def get_by_id(self, weather_id: str) -> Optional[WeatherData]:
        record = self.db.query(WeatherEntity).filter_by(id=weather_id).first()
        return to_weather_data(record) if record else None

    def get_chart_data(
            self,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            sort_by: Optional[List[str]] = None,
    ) -> Tuple[List[WeatherData], int]:

        query = self.db.query(WeatherEntity)

        if start_date:
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(WeatherEntity.time >= start_date)
        if end_date:
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            query = query.filter(WeatherEntity.time <= end_date)

        # Sorting
        if sort_by:
            for item in reversed(sort_by):
                field, _, direction = item.partition(":")
                reverse = direction.lower() == "desc"

                column = getattr(WeatherEntity, field, None)
                if column is not None:
                    query = query.order_by(column.desc() if reverse else column.asc())

        results = query.all()
        total = query.count()
        return [to_weather_data(r) for r in results], total

    def measurement_exists(self, city: str, timestamp: datetime) -> bool:
        return (
            self.db.query(WeatherEntity)
            .filter(WeatherEntity.city == city, WeatherEntity.time == timestamp)
            .first()
            is not None
        )