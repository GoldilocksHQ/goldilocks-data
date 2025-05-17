import json
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

def save_to_json(data: Any, filepath: str) -> None:
    """Saves data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Successfully saved data to {filepath}")
    except IOError as e:
        logger.error(f"Error saving data to {filepath}: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while saving to {filepath}: {e}")
        raise

def load_from_json(filepath: str) -> Any:
    """Loads data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {filepath}")
        return data
    except FileNotFoundError:
        logger.error(f"Error: File not found at {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {filepath}: {e}")
        raise
    except IOError as e:
        logger.error(f"Error loading data from {filepath}: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading from {filepath}: {e}")
        raise 