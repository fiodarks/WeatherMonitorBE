import yaml
from pydantic import BaseModel
from typing import Optional

class AppConfig(BaseModel):
    name: str = "Web app"
    environment: str = "dev"
    repository_type: str = "in-memory"

def load_config() -> AppConfig:
    try:
        """Load YAML config and return a validated AppConfig instance"""
        config_path = "./config.yaml"
        with open(config_path, "r") as f:
            raw_cfg = yaml.safe_load(f)
        app_cfg = raw_cfg.get("app", {})
        return AppConfig(**app_cfg)
    except Exception:
        return AppConfig()
