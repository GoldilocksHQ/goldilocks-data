# Implementation Plan: Concurrent Supabase Uploader

-   **`created_at`**: `2025-06-14`
-   **`updated_at`**: `2025-06-14`
-   **`author`**: `AI Assistant`

## 1. Overview

This document outlines the implementation plan for a new script (`run_supabase_uploader.py`) designed to process JSON files from the systematic Neuron360 search, structure the data, and upload it to Supabase concurrently.

The core requirements are:
-   **Concurrent Processing**: Upload data to Supabase using a configurable number of concurrent workers to maximize throughput.
-   **Resilient File Handling**: The script will process files in a continuous loop, deleting successful files, moving failed files, and periodically re-scanning for new ones.
-   **Auditable Progress**: A detailed CSV log will track the status, contents, and processing time for every file handled.

## 2. Legend

-   `[ ]` To Do: Task has not been started.
-   `[/]` In Progress: Task is actively being worked on.
-   `[x]` Done: Task is complete.
-   `[!]` Blocked: Task is blocked by another task or issue.

## 3. Directory Structure

This implementation will introduce one new script, one new utility, and several new data/log files. The structure will be as follows:

```
goldilocks-data/
├── run_supabase_uploader.py         # New: Main orchestration script.
├── data/
│   ├── supabase_upload_progress.csv # New: CSV log for upload progress.
│   └── neuron360/
│       ├── systematic_search_results/ # Source directory for JSON files.
│       └── failed_uploads/            # New: Directory for failed JSON files.
└── src/
    └── utils/
        └── progress_logger.py         # New: Utility for managing the CSV log.
```

## 4. Implementation Phases

---

### **Phase 1: Core Utilities & Setup**

This foundational phase involves setting up the new script file, creating the progress logging utility, and defining the necessary configurations.

**Tasks:**

-   `[x]` **Create Main Script File (`run_supabase_uploader.py`)**:
    -   Create the new script in the root of `goldilocks-data/`.
    -   Import necessary libraries: `os`, `json`, `shutil`, `concurrent.futures`, `argparse`, `time`, `logging`, and `threading`.
    -   Set up basic logging using the existing logger from `src.utils.logging`.
    -   Define global constants for file paths (source directory, failed directory, progress CSV path).
    -   Implement `argparse` to accept a `--workers` argument, with a default value of 50.
    -   Create a placeholder `main()` function that will orchestrate the process.

-   `[x]` **Create `ProgressLogger` Utility**:
    -   Create a new file at `src/utils/progress_logger.py`.
    -   Implement a `ProgressLogger` class. It must be thread-safe by using `threading.Lock` to manage all read/write operations to the CSV file.
    -   **`__init__`**: The constructor will take the CSV file path and initialize the file with headers (`file_path`, `total_profiles`, `successful_uploads`, `failed_uploads`, `processing_time_seconds`, `status`, `started_at`, `completed_at`) if it doesn't exist. It will also initialize a `threading.Lock`.
    -   **`log_start(file_path, profile_count)`**: This method will acquire the lock and write a new row to the CSV with the initial details, a `status` of `IN_PROGRESS`, and a `started_at` timestamp.
    -   **`log_end(file_path, successful, failed, duration, status)`**: This method will acquire the lock, read the entire CSV, find the matching row for `file_path`, update it in memory, and rewrite the entire file. This ensures atomic updates. The final `status` will be `COMPLETED` or `FAILED`.

---

### **Phase 2: Adapting Managers for File-Based Processing**

This phase focuses on minimally modifying the existing data managers to read from JSON files, preserving the existing data processing logic.

**Tasks:**

-   `[x]` **Modify `PeopleManager`**:
    -   Add a new public method: `process_people_from_file(self, file_path: str) -> tuple[int, int]`.
    -   This method will:
        1.  Open and read the JSON file using `json.load()`. Handle potential `FileNotFoundError` and `json.JSONDecodeError`.
        2.  Extract the list of profiles from the `results` key. If the key is missing or the list is empty, return `(0, 0)`.
        3.  Initialize `success_count = 0` and `failure_count = 0`.
        4.  Iterate through each `person_record` in the list.
        5.  Wrap the call to the existing `self.process_person_data(person_record)` in a `try...except` block.
        6.  If `process_person_data` runs without error, increment `success_count`.
        7.  If it throws an exception, log the error and increment `failure_count`.
        8.  Return the final `(success_count, failure_count)`.

-   `[x]` **Confirm `OrganisationManager` Integration**:
    -   No changes are anticipated for `OrganisationManager`. The existing `PeopleManager.process_person_data` already calls it correctly. This task is to verify during implementation that the existing flow is triggered as expected from the new method.

---

### **Phase 3: Main Orchestration Logic**

This phase implements the core concurrent processing loop in `run_supabase_uploader.py`.

**Tasks:**

-   `[x]` **Implement the Worker Function (`process_file`)**:
    -   Create a standalone function `process_file(file_path, progress_logger)` that will be executed by each thread.
    -   **Crucially, instantiate `OrganisationManager` and `PeopleManager` *inside* this function**. This ensures each thread has its own manager and service instances, which in turn creates a dedicated, thread-safe Supabase client.
    -   Implement the file handling logic as described in the overview:
        -   Read the file to get `profile_count`. If zero, delete the file and return.
        -   Call `progress_logger.log_start()`.
        -   Start a timer.
        -   In a `try...except` block, call `people_manager.process_people_from_file()`.
        -   On success, delete the file (`os.remove`) and log the end state as `COMPLETED`.
        -   On exception, move the file (`shutil.move`) to the failed directory and log the end state as `FAILED`.

-   `[x]` **Implement the Main Controller Loop**:
    -   In the `main` function, initialize the `ProgressLogger`.
    -   Create an infinite `while True` loop.
    -   Inside the loop:
        1.  Scan the source directory for `.json` files.
        2.  If the list of files is empty, log that no new files were found and `break` the loop to exit the script.
        3.  If files are found, create the `concurrent.futures.ThreadPoolExecutor` with the specified number of workers.
        4.  Use `executor.map()` to apply the `process_file` function to the list of file paths.
        5.  After the executor finishes, log that a cycle is complete and loop again to check for any new files that may have arrived.

---

### **Phase 4: Testing and Finalization**

This phase ensures the reliability and correctness of the new pipeline.

**Tasks:**

-   `[ ]` **Unit Tests**:
    -   Write unit tests for `ProgressLogger` to verify thread-safe CSV writing and updating.
    -   Write unit tests for the new `process_people_from_file` method in `PeopleManager`, mocking the file system and the underlying `process_person_data` method to test the counting and error handling logic.
-   `[ ]` **Integration Test**:
    -   Create an integration test that:
        1.  Sets up a temporary directory structure (`source`, `failed`).
        2.  Creates sample JSON files: one valid, one empty, one with invalid JSON.
        3.  Runs `run_supabase_uploader.py` as a subprocess with a small number of workers.
        4.  Asserts that the directories and the progress CSV are in the expected final state (files moved/deleted correctly, log reflects reality).
-   `[ ]` **Update README**:
    -   Add a new section to the main `README.md` explaining how to run the `run_supabase_uploader.py` script, its purpose, and its command-line options.
