from sqlalchemy.exc import SQLAlchemyError

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


    def delete(self, weather_id: str) -> bool:
        record = self.db.query(WeatherEntity).filter_by(id=weather_id).first()
        if not record:
            return False

        self.db.delete(record)
        self.db.commit()
        return True

    def update(self, weather_id: str, measurement: WeatherData) -> Optional[WeatherData]:
        try:
            weather_id_int = int(weather_id)

            # Fetch existing entity
            record = (
                self.db.query(WeatherEntity)
                .filter(WeatherEntity.id == weather_id_int)
                .first()
            )

            if not record:
                print(f"Update failed: record with id {weather_id} not found")
                return None

            record.city = measurement.city
            record.time = measurement.time
            record.temperature_2m = measurement.temperature
            record.temperature_2m_unit = measurement.temperature_unit
            record.is_day = int(measurement.is_day)
            record.rain = measurement.rain
            record.rain_unit = measurement.rain_unit
            record.surface_pressure = measurement.surface_pressure
            record.surface_pressure_unit = measurement.surface_pressure_unit
            record.wind_speed_10m = measurement.wind_speed
            record.wind_speed_10m_unit = measurement.wind_speed_unit

            self.db.commit()
            self.db.refresh(record)

            return to_weather_data(record)

        except Exception as e:
            self.db.rollback()
            print(f"Unexpected error during update: {e}")
            raise
