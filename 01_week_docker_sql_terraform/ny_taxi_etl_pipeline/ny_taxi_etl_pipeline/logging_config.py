import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str = "etl_pipeline.log", log_level: int = logging.INFO):
    """
    Configures logging for the application with console and rotating file handlers.

    Args:
        log_file (str): The name of the log file.
        log_level (int): The logging level (default: INFO).
    """

    # Define log format
    log_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(log_level)

    # Rotating file handler (10 MB max, 5 backup files)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(log_level)

    # Get root logger and configure handlers
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Optional: Disable logging from external libraries (if too verbose)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.info("Logging has been configured successfully.")
