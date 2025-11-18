from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from fastapi.responses import Response
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

from app.adapters.restapi.dependecies import get_measurement_repository
from app.domain.model.weather_data import WeatherData
from app.domain.weather_service import OpenMeteoWeatherService


router = APIRouter(prefix="/api/weather", tags=["Weather Measurements"])


@router.get("/measurements", response_model=WeatherData)
def get_air_quality(
    city: str = "Warsaw",
    repo=Depends(get_measurement_repository),
):
    try:
        service = OpenMeteoWeatherService(measurement_repo=repo)
        result = service.get_latest_measurement(city)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching latest measurement"
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while fetching latest measurement"
        )

    if not result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return result


@router.post("/measurements", response_model=WeatherData, status_code=201)
def add_measurement(
    city: str = Query(...),
    temperature: float = Query(...),
    temperature_unit: str = Query(...),
    is_day: bool = Query(...),
    rain: float = Query(...),
    rain_unit: str = Query(...),
    surface_pressure: float = Query(...),
    surface_pressure_unit: str = Query(...),
    wind_speed: float = Query(...),
    wind_speed_unit: str = Query(...),
    repo=Depends(get_measurement_repository),
):
    try:
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

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while saving measurement"
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while saving measurement"
        )

    return saved


@router.get("/measurements/chart-data", response_model=List[WeatherData])
def get_chart_data(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    sort_by: List[str] = Query(["timestamp:asc"]),
    repo=Depends(get_measurement_repository),
):
    try:
        items, _ = repo.get_chart_data(
            start_date=start_date,
            end_date=end_date,
            sort_by=sort_by,
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching chart data"
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while fetching chart data"
        )

    return items


@router.put("/measurements/{measurement_id}", response_model=WeatherData)
def update_measurement(
    measurement_id: int,
    data: WeatherData,
    repo=Depends(get_measurement_repository),
):
    try:
        existing = repo.get_by_id(measurement_id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Measurement with this ID does not exist",
            )

        updated = repo.update(measurement_id, data)
        print(updated)
        if not updated:
            raise HTTPException(
                status_code=500,
                detail="Failed to update measurement",
            )

        return updated

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while updating measurement: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred while updating measurement: {str(e)}",
        )


@router.delete("/measurements/{measurement_id}", status_code=204)
def delete_measurement(
    measurement_id: int,
    repo=Depends(get_measurement_repository),
):
    try:
        existing = repo.get_by_id(measurement_id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Measurement with this ID does not exist",
            )

        deleted = repo.delete(measurement_id)
        if not deleted:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete measurement",
            )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while deleting measurement: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred while deleting measurement: {str(e)}",
        )

    return Response(status_code=204)
