---
title: Implementation Plan - Systematic Neuron360 Data Extraction
created_at: 2025-06-14
updated_at: 2025-06-14
status: Not Started
---

# Implementation Plan: Systematic Neuron360 Data Extraction

## 1. Context & Objective

This document outlines the implementation plan for creating a robust, systematic data extraction script. The script's primary objective is to exhaustively query and download all available UK-based profile data from the Neuron360 Profile Search API.

The core challenge is the API's limitation of returning a maximum of 10,000 records per query. To overcome this, the script will employ a hierarchical filtering strategy, starting with broad criteria and progressively adding more specific filters until the result set for a given query is less than 10,000. This ensures that all profiles can be captured across numerous, smaller, targeted requests.

The script must be resumable, handle transient network errors gracefully, and provide clear tracking of its progress and any failures.

### Legend for Task Status
-   `[ ]` - To Do
-   `[~]` - In Progress
-   `[x]` - Done
-   `[-]` - Blocked / Won't Do

## 2. Directory & File Structure

This implementation will introduce the following new files and modify existing ones. The structure is designed to align with the existing project architecture.

```
goldilocks-data/
├── data/
│   ├── systematic_request_tracker.csv  # New: Tracks progress of all parameter queries.
│   ├── failed_requests.log             # New: Logs all requests that fail after retries.
│   └── neuron360/
│       └── systematic_search_results/  # New: Root directory for saved JSON responses.
├── doc/
│   └── implementation_plan/
│       └── implementation_plan_systematic_extraction.md # This file.
├── run_systematic_profile_search.py    # New: Main entry point for the script.
└── src/
    ├── config/
    │   └── extraction_config.py        # New: Defines parameter hierarchy and iteration values.
    ├── managers/
    │   └── profile_search_manager.py   # Modified: To support custom output dirs and better error handling.
    ├── services/
    │   └── neuron360_service.py        # Modified: To include 5xx retry logic.
    └── utils/
        ├── progress_tracker.py         # New: Class to manage the progress tracking CSV.
        └── failed_request_logger.py    # New: Module for logging failed requests.
```

## 3. Implementation Phases

The project is divided into five phases, starting with foundational setup and moving through to the core logic, iteration, data handling, and final validation.

### Phase 1: Core Components & Setup

This phase focuses on establishing the foundational structure of the script, including configuration, logging, and the core classes for managing state.

**Tasks:**

-   `[x]` **Create New Script File**:
    -   Create `goldilocks-data/run_systematic_profile_search.py`.
-   `[x]` **Configuration Management**:
    -   Create `src/config/extraction_config.py`. This file will define the parameter hierarchy, iteration values (date ranges, score ranges), and static values (e.g., country). This cleanly separates the script's logic from the query parameters.
-   `[x]` **Progress Tracking Setup**:
    -   Create a new class `ProgressTracker` in `src/utils/progress_tracker.py`.
    -   This class will manage the state in `data/systematic_request_tracker.csv`.
    -   **Columns**: `timestamp`, `parameters_json`, `total_profiles`, `is_workable` (boolean), `status` (`PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`), `last_completed_page`.
    -   It requires methods: `load_progress()`, `log_check()`, `update_page_progress()`, `mark_completed()`, `mark_failed()`.
-   `[x]` **Failed Request Logger**:
    -   Create a simple, dedicated logger in `src/utils/failed_request_logger.py`.
    -   It will be configured to write to `data/failed_requests.log` and log the timestamp, payload, final error, and retry count.

### Phase 2: Enhanced API Interaction & Data Handling

This phase enhances the existing API services for resilience and flexible data storage.

**Tasks:**

-   `[x]` **Update `Neuron360Service` for Resilience**:
    -   Modify `search_profiles` in `src/services/neuron360_service.py`.
    -   Implement a retry loop (3 attempts) for `5xx` server errors. Use an exponential backoff strategy for delays between retries (e.g., 2, 4, 8 seconds).
    -   If all retries fail, the original exception must be re-raised.
-   `[x]` **Update `ProfileSearchManager` for Flexibility & Error Handling**:
    -   Modify `src/managers/profile_search_manager.py`.
    -   Update the `__init__` or `search` method to accept an optional `output_dir` parameter. If provided, responses will be saved there instead of the default `data/neuron360/profile_search`.
    -   The `_save_response_to_file` method should also create subdirectories based on the query parameters (e.g., date/seniority) to keep the output organized.
    -   The `search` method's `except` block should be changed. Instead of catching the exception and returning `None`, it should let the exception propagate up. This allows the calling script to handle the failure explicitly.

### Phase 3: Hierarchical Parameter Generation

This phase implements the core logic for generating the precise sequence of parameter combinations.

**Tasks:**

-   `[x]` **Create `ParameterGenerator` Class**:
    -   Create this class in `run_systematic_profile_search.py` or a new `src/utils/parameter_generator.py` file.
    -   It will import the hierarchy and values from `src/config/extraction_config.py`.
    -   It will contain the nested logic to generate and `yield` one parameter dictionary at a time.
    -   The constructor should accept the `ProgressTracker` instance. Before yielding a parameter set, it will check the tracker and `skip` any that are already marked `COMPLETED`.

### Phase 4: Main Execution Logic

This phase implements the main workflow in `run_systematic_profile_search.py`, orchestrating all other components.

**Tasks:**

-   `[x]` **Implement Main Orchestrator**:
    -   Instantiate `ProgressTracker`, `ProfileSearchManager`, and `ParameterGenerator`.
    -   Loop through the parameter sets from the `ParameterGenerator`.
-   `[x]` **Implement Initial Check & Rate Limiting**:
    -   For each parameter set, make the initial "check" request (`page_size: 1`).
    -   **Add a configurable delay (`time.sleep()`) within this loop** to respect the API rate limit (e.g., default to 70ms for <1000 requests/min).
    -   Call `ProgressTracker.log_check()` with the results.
-   `[x]` **Implement Decision Logic**:
    -   If the check shows the query is "workable" (`total_profiles` < 10,000), proceed to the Mass Request Mode.
    -   If not, the loop continues to the next, more granular parameter set from the generator.
-   `[x]` **Implement Mass Request Mode**:
    -   Calculate the total pages needed.
    -   Determine the starting page using `ProgressTracker`.
    -   Loop through the required pages, calling `ProfileSearchManager.search()` for each.
        -   The `search` method will now raise an exception on failure. The loop must wrap this call in a `try...except` block.
        -   On failure, log the failure with the `FailedRequestLogger` and `ProgressTracker`, then break the loop for this parameter set.
        -   On success, update the page progress in the `ProgressTracker`.
    -   After the loop (either completed or broken by failure), mark the parameter set's final status in the tracker.

### Phase 5: Testing and Validation

-   `[x]` **Unit Tests**:
    -   Write tests for `ProgressTracker` and the `Neuron360Service` retry logic.
-   `[x]` **Integration Test (Dry Run Mode)**:
    -   Add a `--dry-run` command-line argument to `run_systematic_profile_search.py`.
    -   In this mode, the script performs the initial checks but only logs the intent to mass request, without actually doing it. This validates the generator and decision logic.
-   `[ ]` **Full Run Validation**:
    -   Run the script and monitor the tracker CSV and log files.
    -   Manually stop and restart the script to confirm it resumes correctly from the last tracked page.

### Phase 6: Refactoring to Top-Down Execution Logic

This phase will replace the current bottom-up parameter generation with a top-down recursive search algorithm as described in the system design document. This will make the search process more efficient by avoiding queries for highly specific parameter sets when broader criteria already yield a manageable number of results.

-   `[x]` **Deprecate `ParameterGenerator` and Create `ParameterProvider`**:
    -   The `ParameterGenerator` class in `src/utils/parameter_generator.py` will be removed.
    -   A new, simpler `ParameterProvider` class will be created in `src/utils/parameter_provider.py`.
    -   This class will not generate all combinations. Instead, it will have a single method, `get_values_for_layer(layer_name, current_params)`, that returns the list of filter values for a specific hierarchy layer on demand. The logic will be ported from the old `_get_values_for_layer` method.

-   `[x]` **Overhaul Main Execution Logic in `run_systematic_profile_search.py`**:
    -   Remove the main `for` loop that iterates through every possible parameter combination.
    -   Implement a new recursive function, `process_layer(params, layer_index)`. This function will be the new core of the script.

-   `[x]` **Implement `process_layer` Recursive Function**:
    -   The function will accept the `current_params` and the current `layer_index`.
    -   It will loop through the filter values for the current layer (retrieved from `ParameterProvider`).
    -   For each filter value, it will build a `new_params` dictionary.
    -   **Crucially, it will first make a "check" request with `new_params`**.
    -   **Decision Logic**:
        -   If the result count is `< 10,000`, it will trigger the **Mass Request Mode** for `new_params` and then **continue to the next filter in the same layer**. It will NOT recurse deeper.
        -   If the result count is `>= 10,000`, it will log this and **call itself (`process_layer(new_params, layer_index + 1)`) to descend into the next hierarchy layer**.
        -   If the result count is `>= 10,000` at the very last layer of the hierarchy, it will execute the mass request anyway, as specified in the design document.

-   `[x]` **Update Progress Tracking Integration for Full Resumability**:
    -   The `process_layer` function must use the `ProgressTracker` at the beginning of each iteration to achieve robust resumability.
    -   Before making any API call, it will call `tracker.get_progress(new_params)`.
    -   **Resumption Logic**:
        -   If `progress['status'] == 'COMPLETED'`: Log and skip this entire parameter set and its children. `continue` to the next iteration in the current layer.
        -   If `progress['status'] == 'IN_PROGRESS'`: Log and resume the download by calling `mass_request_pages`, which already contains the logic to start from the `last_completed_page`. After completion, `continue` to the next iteration.
        -   If `progress['is_workable'] == 'False' ('SKIPPED_TOO_LARGE')`: The check has already been performed. Do not make another check request. Immediately recurse deeper by calling `process_layer(new_params, layer_index + 1)`.
        -   Only if `progress` is `None` (i.e., this parameter set has never been seen before) will the script perform the "check" API request.
-   `[x]` **Initiate the Flow**:
    -   The `main` function will be simplified to initialize the components (including calling `tracker.load_progress()` at startup) and make the first call to `process_layer({}, 0)` to start the top-down search.

### Phase 7: Concurrent Mass Request Execution

This phase will refactor the script to perform the "mass request" portion of the data extraction concurrently using a pool of worker threads. This will significantly speed up the overall process by decoupling the discovery of workable queries from the time-consuming process of downloading all their pages.

-   `[ ]` **Enhance `ProgressTracker` for Thread Safety**:
    -   Modify `src/utils/progress_tracker.py`.
    -   Introduce a `threading.Lock` as an instance variable in the `__init__` method.
    -   Wrap all methods that perform file I/O (`_initialize_file`, `load_progress`, `_append_to_csv`, and `_rewrite_csv`) with this lock using a `with self.lock:` block. This is the most critical change to prevent data corruption from concurrent writes to the tracking CSV.

-   `[ ]` **Adapt `run_systematic_profile_search.py` for Concurrency**:
    -   Import the `concurrent.futures` module.
    -   Add a new command-line argument, `--threads`, with a default value of `5`. This will allow the user to control the number of concurrent worker threads.
    -   In the `main` function, initialize a `concurrent.futures.ThreadPoolExecutor` and manage it with a `with` statement.
    -   Pass the executor instance to the `process_layer` function.

-   `[ ]` **Refactor Core Execution Logic for Threading**:
    -   Modify the `process_layer` function to accept the `executor` as an argument. When it finds a workable query, it will submit the task to the pool: `executor.submit(mass_request_pages, new_params, total_profiles)`. The logic for resuming `IN_PROGRESS` jobs will be similarly updated.
    -   **Crucially, modify `mass_request_pages` to instantiate its own `ProfileSearchManager`**. This is essential for thread safety, as each thread needs its own `Neuron360Service` and `requests.Session`. The global `MANAGER` instance will only be used by the main thread for the initial, single-threaded "check" queries.

-   `[ ]` **Verify Component Thread Safety (Analysis Task)**:
    -   **`Neuron360Service`**: Re-verify thread safety. (Analysis complete: The service is NOT thread-safe if a single instance is shared. The plan to instantiate a new `ProfileSearchManager` per thread resolves this by giving each thread its own service instance.)
    -   **`ProgressTracker`**: To be made thread-safe with a lock.
    -   **`failed_request_logger`**: Standard Python logger is thread-safe. No changes needed.
    -   This task is to ensure the implementation follows the analysis.

-   `[ ]` **Update Documentation**:
    -   Update the main `README.md` or `doc/systematic_data_extraction.md` to document the new `--threads` command-line argument.
