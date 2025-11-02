from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, Response, Query, HTTPException
from starlette import status

from app.adapters.restapi.dependecies import get_measurement_repository
from app.domain.model.weather_data import WeatherData
from app.domain.weather_service import OpenMeteoWeatherService

router = APIRouter()

@router.get("/weather/measurements", response_model=WeatherData)
def get_air_quality(
    city: str = "Warsaw",
    repo = Depends(get_measurement_repository)
):
    use_case = OpenMeteoWeatherService(measurement_repo=repo)
    new_measurements = use_case.get_latest_measurement(city)
    if not new_measurements:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return new_measurements

@router.post("/weather/measurements", response_model=WeatherData)
def add_measurement(
    city: str = Query(..., example="Warsaw"),
    temperature: float = Query(..., example=12.4),
    temperature_unit: str = Query(..., example="°C"),
    is_day: bool = Query(..., example=True),
    rain: float = Query(..., example=0.0),
    rain_unit: str = Query(..., example="mm"),
    surface_pressure: float = Query(..., example=998.2),
    surface_pressure_unit: str = Query(..., example="hPa"),
    wind_speed: float = Query(..., example=6.8),
    wind_speed_unit: str = Query(..., example="km/h"),
    repo = Depends(get_measurement_repository),
):
    measurement = WeatherData(
        city=city,
        time=datetime.now(timezone.utc).replace(microsecond=0).replace(tzinfo=None),
        temperature=temperature,
        temperature_unit=temperature_unit,
        is_day=is_day,
        rain=rain,
        rain_unit=rain_unit,
        surface_pressure=surface_pressure,
        surface_pressure_unit=surface_pressure_unit,
        wind_speed=wind_speed,
        wind_speed_unit=wind_speed_unit,
    )

    saved = repo.add(measurement)
    return saved

@router.get("/weather/measurements/chart-data", response_model=List[WeatherData])
def get_chart_data(
    start_date: Optional[datetime] = Query(None, description="Filter start date (ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filter end date (ISO)"),
    sort_by: List[str] = Query(["timestamp:asc"], description="Sorting fields"),
    repo = Depends(get_measurement_repository)):

    items, _ = repo.get_chart_data(
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
    )

    return items

