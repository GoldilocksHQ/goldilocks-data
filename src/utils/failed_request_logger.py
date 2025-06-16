import logging
import os
from src.config.path_config import DATA_DIR


def setup_failed_request_logger():
    """
    Sets up a dedicated logger for requests that fail permanently.
    """
    log_dir = DATA_DIR
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("FailedRequestLogger")
    logger.setLevel(logging.ERROR)

    # Prevent the log messages from being propagated to the root logger
    logger.propagate = False

    # Add handler only if it doesn't have one already
    if not logger.handlers:
        handler = logging.FileHandler(os.path.join(log_dir, "failed_requests.log"))
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Instantiate the logger so it can be imported
failed_request_logger = setup_failed_request_logger()
