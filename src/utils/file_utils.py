import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


def save_json_response(
    response: Dict[str, Any], output_dir: str, sub_dir_path: Optional[str] = None
) -> str:
    """
    Saves a dictionary to a timestamped JSON file.
    Args:
        response (dict): The dictionary containing the API response.
        output_dir (str): The base directory where response files will be saved.
        sub_dir_path (str, optional): A path for a sub-directory.
    Returns:
        str: The path to the saved file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

    target_dir = output_dir
    if sub_dir_path:
        target_dir = os.path.join(output_dir, sub_dir_path)

    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, f"profile_search_response_{timestamp}.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response, f, indent=4)
        logger.info(f"Successfully saved API response to {file_path}")
        return file_path
    except IOError as e:
        logger.error(f"Failed to save response to {file_path}: {e}")
        raise
