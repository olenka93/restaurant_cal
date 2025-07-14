import logging
import sys


def setup_logging(level=logging.INFO):
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    root_logger.addHandler(console_handler)

    # Set levels for specific loggers
    logging.getLogger("flask-app").setLevel(level)
    logging.getLogger("bdd-tests").setLevel(level)
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
