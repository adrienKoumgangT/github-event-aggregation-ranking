import os
from pathlib import Path
from typing import TypeVar, Optional, Type, List

from dotenv import load_dotenv

T = TypeVar("T")

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def get_env_var(var_name: str, default: Optional[T] = None, var_type: Type[T] = str, delimiter: str = ",") -> Optional[
    T]:
    """
    Get environment variable with type conversion.

    Args:
        var_name: Name of the environment variable
        default: Default value if variable is not set
        var_type: Type to convert the value to (str, int, float, bool, list)
        delimiter: Delimiter for list type variables

    Returns:
        Converted value or default if not found

    Raises:
        ValueError: If the value cannot be converted to the specified type
    """
    value = os.getenv(var_name)

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
            if isinstance(value, str):
                return [item.strip() for item in value.split(delimiter) if item.strip()]
            return list(value)
        elif var_type == str:
            return str(value)
        else:
            raise ValueError(f"Unsupported var_type: {var_type}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Failed to parse env var '{var_name}' as {var_type.__name__}: {e}")


class Config:
    """Application configuration loaded from environment variables."""

    # Server Configuration
    HOST = get_env_var('HOST', default='0.0.0.0', var_type=str)
    PORT = get_env_var('PORT', default=5000, var_type=int)
    DEBUG = get_env_var('DEBUG', default=False, var_type=bool)

    # YARN Configuration
    YARN_RM_HOST = get_env_var('YARN_RM_HOST', default='10.1.1.144', var_type=str)
    YARN_RM_PORT = get_env_var('YARN_RM_PORT', default=8088, var_type=int)
    YARN_RM_URL = f"http://{YARN_RM_HOST}:{YARN_RM_PORT}"

    # Paths Configuration
    BASE_DIR = Path(__file__).parent.parent
    JOBS_DIR = Path(get_env_var('JOBS_DIR', default=str(BASE_DIR / 'data' / 'jobs'), var_type=str))
    RESULTS_DIR = Path(get_env_var('RESULTS_DIR', default=str(BASE_DIR / 'data' / 'results'), var_type=str))
    LOG_DIR = Path(get_env_var('LOG_DIR', default=str(BASE_DIR / 'logs'), var_type=str))

    # Hadoop Configuration
    HADOOP_HOME = get_env_var('HADOOP_HOME', default='/opt/hadoop', var_type=str)
    HADOOP_CONF_DIR = get_env_var('HADOOP_CONF_DIR', default=f'{HADOOP_HOME}/etc/hadoop', var_type=str)
    HADOOP_JAR_PATH = get_env_var(
        'HADOOP_JAR_PATH',
        default='/home/hadoop/github-event-aggregation-ranking/hadoop/target/hadoop-1.0-SNAPSHOT.jar',
        var_type=str
    )
    HADOOP_MAIN_CLASS = get_env_var('HADOOP_MAIN_CLASS', default='it.unipi.App', var_type=str)
    HADOOP_INPUT_DIR = get_env_var('HADOOP_INPUT_DIR', default='/input', var_type=str)
    HADOOP_OUTPUT_DIR = get_env_var('HADOOP_OUTPUT_DIR', default='/output', var_type=str)

    # Spark Configuration
    SPARK_HOME = get_env_var('SPARK_HOME', default='/opt/spark', var_type=str)
    SPARK_SCRIPT = get_env_var(
        'SPARK_SCRIPT',
        default='/home/hadoop/github-event-aggregation-ranking/spark/main.py',
        var_type=str
    )
    SPARK_MASTER = get_env_var('SPARK_MASTER', default='yarn', var_type=str)
    SPARK_DEPLOY_MODE = get_env_var('SPARK_DEPLOY_MODE', default='cluster', var_type=str)

    # Python Non-Parallel Configuration
    PYTHON_NON_PARALLEL_SCRIPT = get_env_var(
        'PYTHON_NON_PARALLEL_SCRIPT',
        default='/home/hadoop/github-event-aggregation-ranking/python-non-parallel/main.py',
        var_type=str
    )
    PYTHON_EXECUTABLE = get_env_var('PYTHON_EXECUTABLE', default='python3', var_type=str)

    # Job Configuration
    MAX_CONCURRENT_JOBS = get_env_var('MAX_CONCURRENT_JOBS', default=5, var_type=int)
    JOB_TIMEOUT_SECONDS = get_env_var('JOB_TIMEOUT_SECONDS', default=3600, var_type=int)
    JOB_POLL_INTERVAL = get_env_var('JOB_POLL_INTERVAL', default=10, var_type=int)

    # Application Configuration
    APP_NAME = get_env_var('APP_NAME', default='GitHub Event Aggregation Ranking', var_type=str)
    APP_VERSION = get_env_var('APP_VERSION', default='1.0.0', var_type=str)
    SECRET_KEY = get_env_var('SECRET_KEY', default='your-secret-key-here', var_type=str)

    # Logging Configuration
    LOG_LEVEL = get_env_var('LOG_LEVEL', default='INFO', var_type=str)
    LOG_FORMAT = get_env_var(
        'LOG_FORMAT',
        default='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        var_type=str
    )
    LOG_FILE = get_env_var('LOG_FILE', default=str(LOG_DIR / 'app.log'), var_type=str)

    # HDFS Configuration
    HDFS_URL = get_env_var('HDFS_URL', default='hdfs://hdfs-namenode:9000', var_type=str)
    HDFS_USER = get_env_var('HDFS_USER', default='hadoop', var_type=str)

    # YARN Application Configuration
    YARN_APPLICATION_QUEUE = get_env_var('YARN_APPLICATION_QUEUE', default='default', var_type=str)
    YARN_APPLICATION_PRIORITY = get_env_var('YARN_APPLICATION_PRIORITY', default=0, var_type=int)
    YARN_APPLICATION_TYPE = get_env_var('YARN_APPLICATION_TYPE', default='YARN', var_type=str)
    YARN_AM_MEMORY = get_env_var('YARN_AM_MEMORY', default=1024, var_type=int)
    YARN_AM_VCORES = get_env_var('YARN_AM_VCORES', default=1, var_type=int)
    YARN_CONTAINER_MEMORY = get_env_var('YARN_CONTAINER_MEMORY', default=1024, var_type=int)
    YARN_CONTAINER_VCORES = get_env_var('YARN_CONTAINER_VCORES', default=1, var_type=int)
    YARN_MAX_APP_ATTEMPTS = get_env_var('YARN_MAX_APP_ATTEMPTS', default=2, var_type=int)

    # CORS Configuration
    CORS_ORIGINS = get_env_var('CORS_ORIGINS', default='*', var_type=str)
    CORS_METHODS = get_env_var('CORS_METHODS', default='GET,POST,PUT,DELETE,OPTIONS', var_type=str)
    CORS_HEADERS = get_env_var('CORS_HEADERS', default='Content-Type,Authorization', var_type=str)

    # Database Configuration
    DATABASE_PATH = str(BASE_DIR / 'data' / 'jobs.db')
    DATABASE_URL = get_env_var(
        'DATABASE_URL',
        default=f'sqlite:///{DATABASE_PATH}',
        var_type=str
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def create_directories(cls):
        """Create all necessary directories if they don't exist."""
        directories = [cls.JOBS_DIR, cls.RESULTS_DIR, cls.LOG_DIR]
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {directory}: {e}")

    @classmethod
    def validate(cls) -> List[str]:
        """
        Validate the configuration and return a list of warnings/errors.

        Returns:
            List of warning/error messages
        """
        warnings = []

        # Check required paths
        if not cls.HADOOP_JAR_PATH or not Path(cls.HADOOP_JAR_PATH).exists():
            warnings.append(f"HADOOP_JAR_PATH does not exist: {cls.HADOOP_JAR_PATH}")

        if not cls.SPARK_SCRIPT or not Path(cls.SPARK_SCRIPT).exists():
            warnings.append(f"SPARK_SCRIPT does not exist: {cls.SPARK_SCRIPT}")

        if not cls.PYTHON_NON_PARALLEL_SCRIPT or not Path(cls.PYTHON_NON_PARALLEL_SCRIPT).exists():
            warnings.append(f"PYTHON_NON_PARALLEL_SCRIPT does not exist: {cls.PYTHON_NON_PARALLEL_SCRIPT}")

        # Check HADOOP_HOME
        if not cls.HADOOP_HOME or not Path(cls.HADOOP_HOME).exists():
            warnings.append(f"HADOOP_HOME does not exist: {cls.HADOOP_HOME}")

        # Check SPARK_HOME
        if not cls.SPARK_HOME or not Path(cls.SPARK_HOME).exists():
            warnings.append(f"SPARK_HOME does not exist: {cls.SPARK_HOME}")

        # Validate port range
        if not (1 <= cls.PORT <= 65535):
            warnings.append(f"PORT is out of valid range: {cls.PORT}")

        if not (1 <= cls.YARN_RM_PORT <= 65535):
            warnings.append(f"YARN_RM_PORT is out of valid range: {cls.YARN_RM_PORT}")

        # Validate numeric values
        if cls.MAX_CONCURRENT_JOBS < 1:
            warnings.append(f"MAX_CONCURRENT_JOBS must be at least 1, got: {cls.MAX_CONCURRENT_JOBS}")

        if cls.JOB_TIMEOUT_SECONDS < 1:
            warnings.append(f"JOB_TIMEOUT_SECONDS must be at least 1, got: {cls.JOB_TIMEOUT_SECONDS}")

        return warnings

    @classmethod
    def display(cls):
        """Display current configuration (excluding sensitive data)."""
        print("=" * 60)
        print("Current Configuration:")
        print("=" * 60)
        print(f"Server: {cls.HOST}:{cls.PORT} (Debug: {cls.DEBUG})")
        print(f"YARN RM: {cls.YARN_RM_URL}")
        print(f"Hadoop Home: {cls.HADOOP_HOME}")
        print(f"Spark Home: {cls.SPARK_HOME}")
        print(f"Jobs Dir: {cls.JOBS_DIR}")
        print(f"Results Dir: {cls.RESULTS_DIR}")
        print(f"Log Dir: {cls.LOG_DIR}")
        print(f"Max Concurrent Jobs: {cls.MAX_CONCURRENT_JOBS}")
        print(f"Job Timeout: {cls.JOB_TIMEOUT_SECONDS}s")
        print("=" * 60)


# Create directories and validate on import
# Config.create_directories()
warnings = Config.validate()
if warnings:
    print("Configuration warnings:")
    for warning in warnings:
        print(f"  - {warning}")

