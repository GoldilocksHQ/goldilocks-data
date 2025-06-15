import csv
import os
import glob
import json
import logging
import threading
from datetime import datetime
from typing import Dict, Optional, Any

# Define constants for event types
EVENT_CHECK = "CHECK"
EVENT_PAGE_UPDATE = "PAGE_UPDATE"
EVENT_COMPLETED = "COMPLETED"
EVENT_FAILED = "FAILED"
MAX_LEDGER_ROWS = 100000


class ProgressTracker:
    """
    Manages and tracks the state of the systematic data extraction process.
    It uses a robust, append-only ledger for the source of truth and maintains
    a legacy tracker CSV for a simple, current-state view.
    The class is thread-safe.
    """

    def __init__(
        self,
        ledger_base_path: str = "goldilocks-data/data/systematic_request_ledgers/systematic_request_ledger",
        tracker_path: str = "goldilocks-data/data/systematic_request_tracker.csv",
    ):
        self.ledger_base_path = ledger_base_path
        self.tracker_path = tracker_path
        self.current_ledger_path = self._get_or_create_latest_ledger()
        self.ledger_row_count = 0

        self.tracker_fieldnames = [
            "timestamp",
            "parameters_json",
            "total_profiles",
            "is_workable",
            "status",
            "last_completed_page",
        ]
        self.ledger_fieldnames = [
            "timestamp",
            "parameters_key",
            "event_type",
            "data_json",
        ]

        self.progress_data: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self._initialize_tracker_file()

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

    def _initialize_tracker_file(self):
        """Creates the legacy tracker CSV with a header if it doesn't exist."""
        if not os.path.exists(self.tracker_path):
            with open(self.tracker_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.tracker_fieldnames)
                writer.writeheader()

    def _get_params_key(self, params: Dict) -> str:
        """Creates a consistent, sorted JSON string to use as a key."""
        return json.dumps(params, sort_keys=True)

    def _rewrite_tracker_file(self):
        """Rewrites the legacy tracker file with the current in-memory state."""
        rows = []
        for key, data in self.progress_data.items():
            rows.append(
                {
                    "timestamp": data.get("timestamp", datetime.now().isoformat()),
                    "parameters_json": key,
                    "total_profiles": data.get("total_profiles", 0),
                    "is_workable": data.get("is_workable", False),
                    "status": data.get("status", "UNKNOWN"),
                    "last_completed_page": data.get("last_completed_page", 0),
                }
            )

        with open(self.tracker_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.tracker_fieldnames)
            writer.writeheader()
            writer.writerows(rows)

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
            is_workable = data["is_workable"]
            total_profiles = data.get("total_profiles", 0)
            status = "SKIPPED_TOO_LARGE"
            if is_workable:
                status = "PENDING"
            elif total_profiles == 0:
                status = "SKIPPED_NO_RESULT"

            self.progress_data[key].update(
                {
                    "total_profiles": total_profiles,
                    "is_workable": is_workable,
                    "status": status,
                    "last_completed_page": 0,
                }
            )
        elif event_type == EVENT_PAGE_UPDATE:
            self.progress_data[key]["last_completed_page"] = data["page_number"]
            self.progress_data[key]["status"] = "IN_PROGRESS"
        elif event_type == EVENT_COMPLETED:
            self.progress_data[key]["status"] = "COMPLETED"
        elif event_type == EVENT_FAILED:
            self.progress_data[key]["status"] = "FAILED"

    def _log_event(self, params: Dict, event_type: str, data: Dict):
        """Central method to log an event, update state, and rewrite files."""
        with self.lock:
            key = self._get_params_key(params)
            event_time = datetime.now().isoformat()

            # This is a bit of a hack to get the row into memory before processing
            # In a real scenario you would have a more complex state machine
            if key not in self.progress_data:
                self.progress_data[key] = {}

            # Special status handling for CHECK events
            if event_type == EVENT_CHECK:
                is_workable = data.get("is_workable", False)
                total_profiles = data.get("total_profiles", 0)
                if not is_workable and total_profiles == 0:
                    # Overwrite the status in the in-memory data before logging
                    if key in self.progress_data:
                        self.progress_data[key]["status"] = "SKIPPED_NO_RESULT"

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
            # Rewrite the simple tracker CSV
            self._rewrite_tracker_file()

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

    def mark_failed(self, params: Dict):
        """Logs that a parameter set has failed."""
        self._log_event(params, EVENT_FAILED, {})

    def get_progress(self, params: Dict) -> Optional[Dict]:
        """Gets the reconstructed progress from the in-memory state."""
        key = self._get_params_key(params)
        with self.lock:
            return self.progress_data.get(key)
