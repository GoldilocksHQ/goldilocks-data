import csv
import os
import threading
from datetime import datetime


class ProgressLogger:
    """
    Manages logging the progress of file uploads to a CSV file in a thread-safe manner.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.fieldnames = [
            "file_path",
            "total_profiles",
            "successful_uploads",
            "failed_uploads",
            "processing_time_seconds",
            "status",
            "started_at",
            "completed_at",
        ]
        self._initialize_file()

    def _initialize_file(self):
        """Creates the CSV file with a header if it doesn't exist."""
        with self.lock:
            if not os.path.exists(self.file_path):
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                with open(self.file_path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                    writer.writeheader()

    def log_start(self, file_path: str, profile_count: int):
        """Logs the start of processing for a file."""
        with self.lock:
            with open(self.file_path, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(
                    {
                        "file_path": file_path,
                        "total_profiles": profile_count,
                        "status": "IN_PROGRESS",
                        "started_at": datetime.now().isoformat(),
                    }
                )

    def log_end(
        self, file_path: str, successful: int, failed: int, duration: float, status: str
    ):
        """Updates the log for a file that has finished processing."""
        with self.lock:
            rows = []
            updated = False
            with open(self.file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["file_path"] == file_path:
                        row["successful_uploads"] = successful
                        row["failed_uploads"] = failed
                        row["processing_time_seconds"] = round(duration, 2)
                        row["status"] = status
                        row["completed_at"] = datetime.now().isoformat()
                        updated = True
                    rows.append(row)

            # If for some reason log_start was never called, add a new row
            if not updated:
                rows.append(
                    {
                        "file_path": file_path,
                        "total_profiles": successful + failed,
                        "successful_uploads": successful,
                        "failed_uploads": failed,
                        "processing_time_seconds": round(duration, 2),
                        "status": status,
                        "completed_at": datetime.now().isoformat(),
                    }
                )

            with open(self.file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
