import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config.settings import Config


def setup_logger(name: str = None) -> logging.Logger:
    """Setup and configure logger"""

    # Create logs directory if it doesn't exist
    log_dir = Config.LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        filename=log_dir / 'app.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Error file handler
    error_handler = RotatingFileHandler(
        filename=log_dir / 'error.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module"""
    return setup_logger(name)
