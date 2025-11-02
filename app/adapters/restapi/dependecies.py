from contextlib import contextmanager

from app.domain.model.config import load_config
from app.persistance.model.weather_entity import SessionLocal
from app.persistance.repositories.in_memory_repository import InMemoryWeatherMeasurementRepository
from app.persistance.repositories.sql_measurement_repository import SQLMeasurementRepository

configs = load_config()
_in_memory = InMemoryWeatherMeasurementRepository()

def get_measurement_repository():
    repo_type = getattr(configs, "repository_type", "in-memory")
    print(f"[Dependency] repo_type = {repo_type}")

    if repo_type == "postgres":
        db = SessionLocal()
        try:
            print("[Dependency] Using SQL repo")
            yield SQLMeasurementRepository(db)
        finally:
            db.close()
    elif repo_type == "in-memory":
        print("[Dependency] Using in-memory repo")
        yield _in_memory
