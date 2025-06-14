import logging
import os
from logging.handlers import RotatingFileHandler
from src.utils.config import config


def setup_logging():
    """
    Sets up the logging for the application.
    """
    log_dir = os.path.dirname(config.LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger("goldilocks")
    logger.setLevel(config.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = RotatingFileHandler(config.LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


logger = setup_logging()
