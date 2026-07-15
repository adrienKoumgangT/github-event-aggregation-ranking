import os
from pathlib import Path
from typing import TypeVar, Optional, Type

import yaml

T = TypeVar("T")


def load_config(config_path: Path):
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Failed to load config from {config_path}: {e}")
        return {}

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

    # Yarn
    YARN_RM_URL = "http://10.1.1.144:8088"

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    JOBS_DIR = BASE_DIR / 'data' / 'jobs'
    RESULTS_DIR = BASE_DIR / 'data' / 'results'
    LOG_DIR = BASE_DIR / 'logs'

    # Hadoop configuration
    HADOOP_HOME = os.getenv('HADOOP_HOME', '/opt/hadoop')
    HADOOP_JAR_PATH = os.getenv('HADOOP_JAR_PATH', '/home/hadoop/github-event-aggregation-ranking/hadoop/target/hadoop-1.0-SNAPSHOT.jar')
    HADOOP_MAIN_CLASS = os.getenv('HADOOP_MAIN_CLASS', 'it.unipi.App')
    HADOOP_INPUT_DIR = os.getenv('HADOOP_INPUT_DIR', '/input')
    HADOOP_OUTPUT_DIR = os.getenv('HADOOP_OUTPUT_DIR', '/output')

    # Spark configuration
    SPARK_HOME = os.getenv('SPARK_HOME', '/opt/spark')
    SPARK_SCRIPT = os.getenv('SPARK_SCRIPT', '/home/hadoop/github-event-aggregation-ranking/spark/main.py')

    # Python non-parallel
    PYTHON_NON_PARALLEL_SCRIPT = os.getenv('PYTHON_NON_PARALLEL_SCRIPT', '/home/hadoop/github-event-aggregation-ranking/python-non-parallel/main.py')

    # Job configuration
    MAX_CONCURRENT_JOBS = int(os.getenv('MAX_CONCURRENT_JOBS', 5))
    JOB_TIMEOUT_SECONDS = int(os.getenv('JOB_TIMEOUT_SECONDS', 3600))

    # Create directories if they don't exist
    for directory in [JOBS_DIR, RESULTS_DIR, LOG_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
