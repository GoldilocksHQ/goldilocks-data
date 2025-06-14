import logging
import time
import requests
from src.utils.config import config

logger = logging.getLogger(__name__)


class Neuron360Service:
    """
    A service for interacting with the Neuron360 API.
    """

    def __init__(self):
        """
        Initializes the Neuron360Service with the API key and URL from config.
        """
        self.api_key = config.NEURON360_API_KEY
        self.base_url = config.NEURON360_API_URL
        if not self.api_key or not self.base_url:
            raise ValueError("NEURON360_API_KEY and NEURON360_API_URL must be set.")
        self.search_url = f"{self.base_url}/profile/search"

    def search_profiles(self, payload: dict) -> dict:
        """
        Performs a profile search using the Neuron360 API with a retry mechanism.

        Args:
            payload (dict): The search parameters payload.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: For network-related errors.
            ValueError: For non-200 responses or invalid JSON.
        """
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        logger.info(f"Sending request to {self.search_url}")

        last_exception = None
        for attempt in range(3):
            try:
                response = requests.post(
                    self.search_url, headers=headers, json=payload, timeout=30
                )
                # Raise HTTPError for bad responses (4xx or 5xx)
                response.raise_for_status()

                try:
                    return response.json()
                except requests.exceptions.JSONDecodeError as exc:
                    logger.error("Failed to decode JSON from response.")
                    raise ValueError("Invalid JSON response from API.") from exc

            except requests.exceptions.RequestException as e:
                last_exception = e
                # Check if the error is a 5xx server error
                if (
                    hasattr(e, "response")
                    and e.response is not None
                    and 500 <= e.response.status_code < 600
                ):
                    wait_time = 2**attempt  # Exponential backoff
                    logger.warning(
                        f"Attempt {attempt + 1}/3 failed with server error: {e}. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    # For non-5xx errors, fail immediately
                    logger.error(
                        "Request to Neuron360 API failed with non-retryable "
                        f"error: {e}"
                    )
                    raise

        # If all retries fail, raise the last captured exception
        logger.error("All retry attempts failed.")
        raise last_exception
