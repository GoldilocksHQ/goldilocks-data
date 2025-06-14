import csv
import os
import json
from datetime import datetime
from typing import Dict, Optional


class ProgressTracker:
    """
    Manages the state of the systematic data extraction in a CSV file,
    allowing the process to be resumed.
    """

    def __init__(self, file_path: str = "data/systematic_request_tracker.csv"):
        self.file_path = file_path
        self.file_exists = os.path.exists(self.file_path)
        self.fieldnames = [
            "timestamp",
            "parameters_json",
            "total_profiles",
            "is_workable",
            "status",
            "last_completed_page",
        ]
        self.progress_data: Dict[str, Dict] = {}
        self._initialize_file()

    def _initialize_file(self):
        """Creates the CSV file with a header if it doesn't exist."""
        if not self.file_exists:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
            self.file_exists = True

    def load_progress(self):
        """Loads the existing progress from the CSV file into memory."""
        try:
            with open(self.file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Use the parameter set as a unique key
                    key = row["parameters_json"]
                    self.progress_data[key] = row
        except FileNotFoundError:
            self._initialize_file()  # Ensure file is created if deleted

    def _get_row_key(self, params: Dict) -> str:
        """Creates a consistent, sorted JSON string to use as a key."""
        return json.dumps(params, sort_keys=True)

    def log_check(self, params: Dict, total_profiles: int, is_workable: bool):
        """Logs the result of an initial query check."""
        key = self._get_row_key(params)
        row = {
            "timestamp": datetime.now().isoformat(),
            "parameters_json": key,
            "total_profiles": total_profiles,
            "is_workable": is_workable,
            "status": "PENDING" if is_workable else "SKIPPED_TOO_LARGE",
            "last_completed_page": 0,
        }
        self.progress_data[key] = row
        self._append_to_csv(row)

    def update_page_progress(self, params: Dict, page_number: int):
        """Updates the last completed page for a given parameter set."""
        key = self._get_row_key(params)
        if key in self.progress_data:
            self.progress_data[key]["last_completed_page"] = page_number
            self.progress_data[key]["status"] = "IN_PROGRESS"
            # This is inefficient but simple. A better way would be to rewrite the file.
            self._rewrite_csv()

    def mark_completed(self, params: Dict):
        """Marks a parameter set as fully completed."""
        key = self._get_row_key(params)
        if key in self.progress_data:
            self.progress_data[key]["status"] = "COMPLETED"
            self._rewrite_csv()

    def mark_failed(self, params: Dict):
        """Marks a parameter set as failed."""
        key = self._get_row_key(params)
        if key in self.progress_data:
            self.progress_data[key]["status"] = "FAILED"
            self._rewrite_csv()

    def get_progress(self, params: Dict) -> Optional[Dict]:
        """Gets the progress for a specific parameter set."""
        key = self._get_row_key(params)
        return self.progress_data.get(key)

    def _append_to_csv(self, row: Dict):
        """Appends a new row to the CSV."""
        with open(self.file_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)

    def _rewrite_csv(self):
        """Rewrites the entire CSV file with the in-memory data."""
        with open(self.file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.progress_data.values())
