from src.utils.logging import logger


class BaseManager:
    """
    A base manager class providing common functionality for all data managers.
    This includes logging and a consistent interface for processing data.
    """

    def __init__(self):
        self.logger = logger
        self.logger.info(f"{self.__class__.__name__} initialized.")

    def process(self, data):
        """
        A placeholder for the main processing logic in subclasses.
        This method should be overridden by each specific manager.
        """
        raise NotImplementedError(
            "The 'process' method must be implemented by subclasses."
        )

    def _log_success(self, message):
        """
        Logs a success message.
        """
        self.logger.info(message)

    def _log_error(self, message, exc_info=False):
        """
        Logs an error message.
        """
        self.logger.error(message, exc_info=exc_info)
