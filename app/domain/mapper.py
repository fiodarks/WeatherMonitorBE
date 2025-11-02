from app.domain.model.weather_data import WeatherData
from app.persistance.model.weather_entity import WeatherEntity


def to_weather_entity(domain: WeatherData) -> WeatherEntity:
    return WeatherEntity(
        city=domain.city,
        time=domain.time,
        temperature_2m=domain.temperature,
        temperature_2m_unit=domain.temperature_unit,
        is_day=int(domain.is_day),
        rain=domain.rain,
        rain_unit=domain.rain_unit,
        surface_pressure=domain.surface_pressure,
        surface_pressure_unit=domain.surface_pressure_unit,
        wind_speed_10m=domain.wind_speed,
        wind_speed_10m_unit=domain.wind_speed_unit,
    )
