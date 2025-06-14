import logging
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
        Performs a profile search using the Neuron360 API.

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
        try:
            response = requests.post(
                self.search_url, headers=headers, json=payload, timeout=30
            )
            response.raise_for_status()

            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as exc:
                logger.error("Failed to decode JSON from response.")
                raise ValueError("Invalid JSON response from API.") from exc

        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Neuron360 API failed: {e}")
            raise
