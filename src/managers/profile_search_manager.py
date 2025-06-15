import os
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

import requests

from src.services.neuron360_service import Neuron360Service

logger = logging.getLogger(__name__)


class ProfileSearchManager:
    """
    Manages searching for profiles using the Neuron360 API, handling
    parameter construction, pagination, and response storage.
    """

    def __init__(self, output_dir: str = "data/neuron360/profile_search"):
        """
        Initializes the manager and the underlying Neuron360 service.
        Args:
            output_dir (str): The directory where response files will be saved.
        """
        self.neuron360_service = Neuron360Service()
        self.response_dir = output_dir
        os.makedirs(self.response_dir, exist_ok=True)

    def _save_response_to_file(
        self, response: dict, sub_dir_path: Optional[str] = None
    ) -> str:
        """
        Saves the API response to a timestamped JSON file.
        Args:
            response (dict): The dictionary containing the API response.
            sub_dir_path (str, optional): A path for a sub-directory.
        Returns:
            str: The path to the saved file.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

        target_dir = self.response_dir
        if sub_dir_path:
            target_dir = os.path.join(self.response_dir, sub_dir_path)
            os.makedirs(target_dir, exist_ok=True)

        file_path = os.path.join(
            target_dir, f"profile_search_response_{timestamp}.json"
        )
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(response, f, indent=4)
            logger.info(f"Successfully saved API response to {file_path}")
            return file_path
        except IOError as e:
            logger.error(f"Failed to save response to {file_path}: {e}")
            raise

    def get_total_profiles(self, response: dict) -> int:
        """
        Extracts the total number of available profiles from a raw API response.

        Args:
            response (dict): The raw dictionary from the API.

        Returns:
            int: The total number of profiles found, or 0 if not present.
        """
        if not isinstance(response, dict):
            return 0
        return response.get("counts", {}).get("profiles_total_results", 0)

    def search(
        self,
        page_number: int = 1,
        page_size: int = 100,
        parameters: Optional[Dict[str, Any]] = None,
        output_sub_dir: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Builds and executes a profile search query, then saves the response.
        It accepts filter parameters as kwargs (e.g., `job_titles=["SE"]`)
        or a complete `parameters` dictionary for complex queries.
        Enum members are automatically converted to their string values.
        Args:
            page_number (int): The page number for pagination (1-100).
            page_size (int): The number of results per page (1-100).
            parameters (dict, optional): A pre-built dictionary of search params.
            output_sub_dir (str, optional): Sub-directory to save response in.
            **kwargs: Search filter parameters for simple key-value searches.
        Returns:
            A dictionary containing the API response.
        Raises:
            requests.exceptions.RequestException: If the request fails after retries.
            ValueError: If the input parameters are invalid.
        """
        if not 1 <= page_size <= 100:
            msg = "page_size must be between 1 and 100."
            logger.error(f"Invalid page_size: {page_size}. {msg}")
            raise ValueError(msg)
        if not 1 <= page_number <= 100:
            msg = "page_number must be between 1 and 100."
            logger.error(f"Invalid page_number: {page_number}. {msg}")
            raise ValueError(msg)

        if parameters:
            api_params = parameters.copy()
        else:
            api_params = {}
            for key, value in kwargs.items():
                if value is None:
                    continue

                if isinstance(value, list):
                    api_params[key] = [
                        v.value if isinstance(v, Enum) else v for v in value
                    ]
                elif isinstance(value, Enum):
                    api_params[key] = value.value
                else:
                    api_params[key] = value

        payload = {
            "reveal_all_data": False,
            "page_number": page_number,
            "page_size": page_size,
            "parameters": api_params,
        }

        log_payload = json.dumps(payload, indent=2, default=str)
        logger.info(f"Searching profiles with payload: {log_payload}")

        try:
            response_data = self.neuron360_service.search_profiles(payload)
            if response_data:
                self._save_response_to_file(response_data, sub_dir_path=output_sub_dir)
            return response_data
        except (requests.exceptions.RequestException, ValueError) as e:
            # Re-raise the exception to be handled by the caller
            logger.error(
                f"Profile search failed for payload: {log_payload}. Error: {e}"
            )
            raise
