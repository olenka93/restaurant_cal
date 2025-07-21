import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def setup_logging(
    level=logging.INFO, log_to_file=False, log_file_path=None, logger_name=None
):
    """
    Configure logging with flexible output options.

    Args:
        level: Logging level (default: logging.INFO)
        log_to_file: Boolean flag to enable/disable file logging (default: False)
        log_file_path: Path to the log file (optional, used only if log_to_file is True)
        logger_name: Name of the logger to configure (optional, configures root logger if None)
    """
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(logger_name) if logger_name else logging.getLogger()
    logger.setLevel(level)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_to_file and log_file_path:
        log_dir = os.path.dirname(log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            delay=True,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
