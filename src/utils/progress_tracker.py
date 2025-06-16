import csv
import os
import glob
import json
import logging
import threading
from datetime import datetime
from typing import Dict, Optional, Any

from src.config.path_config import LEDGER_DIR

# Define constants for event types
EVENT_CHECK = "CHECK"
EVENT_PAGE_UPDATE = "PAGE_UPDATE"
EVENT_COMPLETED = "COMPLETED"
EVENT_FAILED = "FAILED"
MAX_LEDGER_ROWS = 100000


class ProgressTracker:
    """
    Manages and tracks the state of the systematic data extraction process.
    It uses a robust, append-only ledger for the source of truth.
    The class is thread-safe.
    """

    def __init__(
        self,
        ledger_base_path: str = os.path.join(LEDGER_DIR, "systematic_request_ledger"),
    ):
        self.ledger_base_path = ledger_base_path
        self.ledger_fieldnames = [
            "timestamp",
            "parameters_key",
            "event_type",
            "data_json",
        ]
        self.current_ledger_path = self._get_or_create_latest_ledger()
        self.ledger_row_count = 0

        self.progress_data: Dict[str, Dict] = {}
        self.lock = threading.Lock()

    def _get_or_create_latest_ledger(self) -> str:
        """Finds the latest ledger file or creates a new one."""
        ledger_dir = os.path.dirname(self.ledger_base_path)
        os.makedirs(ledger_dir, exist_ok=True)
        ledger_pattern = f"{self.ledger_base_path}*.csv"
        ledger_files = sorted(glob.glob(ledger_pattern))

        if not ledger_files:
            return self._create_new_ledger()

        latest_ledger = ledger_files[-1]
        # Simple row count check to initialize.
        with open(latest_ledger, "r") as f:
            self.ledger_row_count = sum(1 for _ in f) - 1  # Exclude header
        return latest_ledger

    def _create_new_ledger(self) -> str:
        """Creates a new, timestamped ledger file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_ledger_path = f"{self.ledger_base_path}_{timestamp}.csv"
        with open(new_ledger_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.ledger_fieldnames)
            writer.writeheader()
        self.ledger_row_count = 0
        return new_ledger_path

    def _get_params_key(self, params: Dict) -> str:
        """Creates a consistent, sorted JSON string to use as a key."""
        return json.dumps(params, sort_keys=True)

    def _append_event(
        self, key: str, event_type: str, data: Dict[str, Any], event_time: str
    ):
        """Appends a new event to the current ledger file."""
        if self.ledger_row_count >= MAX_LEDGER_ROWS:
            self.current_ledger_path = self._create_new_ledger()

        row = {
            "timestamp": event_time,
            "parameters_key": key,
            "event_type": event_type,
            "data_json": json.dumps(data),
        }
        with open(self.current_ledger_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.ledger_fieldnames)
            writer.writerow(row)
        self.ledger_row_count += 1

    def load_progress(self):
        """
        Loads all ledger files in order and reconstructs the current state.
        """
        ledger_pattern = f"{self.ledger_base_path}*.csv"
        ledger_files = sorted(glob.glob(ledger_pattern))

        for file_path in ledger_files:
            try:
                with open(file_path, "r", newline="") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self._process_event_row(row)
            except Exception as e:
                logging.error(f"Error processing ledger file {file_path}: {e}")

    def _process_event_row(self, row: Dict[str, str]):
        """Processes a single event row to update the in-memory state."""
        key = row["parameters_key"]
        event_type = row["event_type"]
        data = json.loads(row["data_json"])
        timestamp = row["timestamp"]

        if key not in self.progress_data:
            self.progress_data[key] = {}

        self.progress_data[key]["timestamp"] = timestamp

        if event_type == EVENT_CHECK:
            # A CHECK event re-validates a query. Update its workable status
            # and total_profiles, but preserve its page-level progress.
            is_workable = data["is_workable"]
            total_profiles = data.get("total_profiles", 0)
            current_status = self.progress_data[key].get("status")

            self.progress_data[key]["total_profiles"] = total_profiles
            self.progress_data[key]["is_workable"] = is_workable

            # Only reset the status if it's not in a protected state (i.e., already
            # running or finished). This allows retrying FAILED queries.
            if current_status not in ["COMPLETED", "IN_PROGRESS"]:
                new_status = "SKIPPED_TOO_LARGE"
                if is_workable:
                    new_status = "PENDING"
                elif total_profiles == 0:
                    new_status = "SKIPPED_NO_RESULT"
                self.progress_data[key]["status"] = new_status

            # IMPORTANT: Ensure last_completed_page is initialized only if it's not already set.
            if "last_completed_page" not in self.progress_data[key]:
                self.progress_data[key]["last_completed_page"] = 0
        elif event_type == EVENT_PAGE_UPDATE:
            self.progress_data[key]["last_completed_page"] = data["page_number"]
            self.progress_data[key]["status"] = "IN_PROGRESS"
        elif event_type == EVENT_COMPLETED:
            self.progress_data[key]["status"] = "COMPLETED"
        elif event_type == EVENT_FAILED:
            self.progress_data[key]["status"] = "FAILED"
            if "failed_at_page" in data:
                self.progress_data[key]["failed_at_page"] = data["failed_at_page"]

    def _log_event(self, params: Dict, event_type: str, data: Dict):
        """Central method to log an event, update state, and rewrite files."""
        with self.lock:
            key = self._get_params_key(params)
            event_time = datetime.now().isoformat()

            # Process the event to update the in-memory state
            self._process_event_row(
                {
                    "parameters_key": key,
                    "event_type": event_type,
                    "data_json": json.dumps(data),
                    "timestamp": event_time,
                }
            )
            # Append event to the ledger
            self._append_event(key, event_type, data, event_time)

    def log_check(self, params: Dict, total_profiles: int, is_workable: bool):
        """Logs the result of an initial query check."""
        data = {"total_profiles": total_profiles, "is_workable": is_workable}
        self._log_event(params, EVENT_CHECK, data)

    def update_page_progress(self, params: Dict, page_number: int):
        """Logs that a page has been successfully processed."""
        data = {"page_number": page_number}
        self._log_event(params, EVENT_PAGE_UPDATE, data)

    def mark_completed(self, params: Dict):
        """Logs that a parameter set has been fully completed."""
        self._log_event(params, EVENT_COMPLETED, {})

    def mark_failed(self, params: Dict, data: Dict = None):
        """Logs that a parameter set has failed, with optional data."""
        if data is None:
            data = {}
        self._log_event(params, EVENT_FAILED, data)

    def get_progress(self, params: Dict) -> Optional[Dict]:
        """Gets the reconstructed progress from the in-memory state."""
        key = self._get_params_key(params)
        with self.lock:
            return self.progress_data.get(key)
