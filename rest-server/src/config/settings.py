import os
from pathlib import Path
from typing import TypeVar, Optional, Type

T = TypeVar("T")

def get_env_var(var_name: str, default: Optional[T] = None, var_type: Type[T] = str, delimiter: str = ","):
    value = os.getenv(var_name, default)

    if value is None:
        return default

    try:
        if var_type == bool:
            return str(value).strip().lower() in ("true", "1", "yes", "on")
        elif var_type == int:
            return int(value)
        elif var_type == float:
            return float(value)
        elif var_type == list:
            return [item.strip() for item in value.split(delimiter)]
        elif var_type == str:
            return str(value)
        else:
            raise ValueError(f"Unsupported var_type: {var_type}")
    except Exception as e:
        raise ValueError(f"Failed to parse env var '{var_name}' as {var_type.__name__}: {e}")


class Config:
    # Server configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = get_env_var('PORT', default=5000, var_type=int)
    DEBUG = get_env_var('DEBUG', default=True, var_type=bool)

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    JOBS_DIR = BASE_DIR / 'data' / 'jobs'
    RESULTS_DIR = BASE_DIR / 'data' / 'results'
    LOG_DIR = BASE_DIR / 'logs'

    # Create directories if they don't exist
    for directory in [JOBS_DIR, RESULTS_DIR, LOG_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
