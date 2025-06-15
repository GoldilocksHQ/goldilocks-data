import csv
import os
import json
from datetime import datetime

# --- Configuration ---
# Path to the old tracker file to read from
OLD_TRACKER_PATH = "goldilocks-data/data/systematic_request_tracker.csv"
# Path to the new ledger file to write to.
# A timestamp will be appended to this to create the first ledger file.
LEDGER_BASE_PATH = (
    "goldilocks-data/data/systematic_request_ledgers/systematic_request_ledger"
)
# --- End Configuration ---


def migrate_data():
    """
    Reads data from the old CSV tracker and converts it into events
    for the new append-only ledger.
    """
    print("--- Starting Migration from Tracker to Ledger ---")

    if not os.path.exists(OLD_TRACKER_PATH):
        print(f"ERROR: Old tracker file not found at '{OLD_TRACKER_PATH}'. Aborting.")
        return

    # Create the first ledger file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_ledger_path = f"{LEDGER_BASE_PATH}_{timestamp}.csv"
    ledger_fieldnames = ["timestamp", "parameters_key", "event_type", "data_json"]

    events_to_write = []

    print(f"Reading from {OLD_TRACKER_PATH}...")
    with open(OLD_TRACKER_PATH, "r", newline="") as f_old:
        reader = csv.DictReader(f_old)
        for row in reader:
            try:
                params_key = row["parameters_json"]
                status = row["status"]
                event_time = row["timestamp"]
                total_profiles = int(row["total_profiles"])
                is_workable = row["is_workable"].lower() == "true"
                last_page = int(row["last_completed_page"])

                # Event 1: The initial check is always created
                check_data = {
                    "total_profiles": total_profiles,
                    "is_workable": is_workable,
                }
                events_to_write.append(
                    {
                        "timestamp": event_time,
                        "parameters_key": params_key,
                        "event_type": "CHECK",
                        "data_json": json.dumps(check_data),
                    }
                )

                # Event 2: Page updates for IN_PROGRESS or COMPLETED tasks
                if status in ["IN_PROGRESS", "COMPLETED"] and last_page > 0:
                    # We only have the *last* page, so we create one event for it.
                    page_data = {"page_number": last_page}
                    events_to_write.append(
                        {
                            "timestamp": event_time,
                            "parameters_key": params_key,
                            "event_type": "PAGE_UPDATE",
                            "data_json": json.dumps(page_data),
                        }
                    )

                # Event 3: A final status event
                if status == "COMPLETED":
                    events_to_write.append(
                        {
                            "timestamp": event_time,
                            "parameters_key": params_key,
                            "event_type": "COMPLETED",
                            "data_json": json.dumps({}),
                        }
                    )
                elif status == "FAILED":
                    events_to_write.append(
                        {
                            "timestamp": event_time,
                            "parameters_key": params_key,
                            "event_type": "FAILED",
                            "data_json": json.dumps({}),
                        }
                    )
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"Skipping malformed row: {row}. Error: {e}")
                continue

    # Sort events by timestamp to maintain chronological order
    events_to_write.sort(key=lambda x: x["timestamp"])

    print(f"Writing {len(events_to_write)} events to {new_ledger_path}...")
    os.makedirs(os.path.dirname(new_ledger_path), exist_ok=True)
    with open(new_ledger_path, "w", newline="") as f_new:
        writer = csv.DictWriter(f_new, fieldnames=ledger_fieldnames)
        writer.writeheader()
        writer.writerows(events_to_write)

    print("--- Migration Finished Successfully ---")


if __name__ == "__main__":
    migrate_data()
