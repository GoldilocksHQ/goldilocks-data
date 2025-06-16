---
title: "Systematic Extractor Refactoring for Performance and Correctness"
created_at: "2025-06-15"
updated_at: "2025-06-15"
---

# Systematic Extractor Refactoring Plan

## 1. Overview & Goals

This document outlines the plan to refactor the systematic data extraction script. The script currently suffers from two major issues:

1.  **Critical Correctness Bug**: A logic flaw in the restart mechanism causes the script to terminate prematurely by incorrectly pruning entire branches of the search hierarchy. It also wastes resources by exploring branches that are known to be empty.
2.  **Severe Performance Bottleneck**: The script's throughput is limited to ~30 responses per minute due to synchronous file I/O and progress logging directly within the high-volume worker threads.

The goals of this refactoring are:
-   **Correctness**: Ensure the script reliably explores all parameter combinations to completion, correctly handling all possible states on a restart.
-   **Performance**: Increase the data extraction throughput to a target of at least 200 responses per minute by decoupling I/O operations from network requests.

## 2. Status Legend

-   `[ ] PENDING`: The task has not been started.
-   `[~] IN PROGRESS`: The task is actively being worked on.
-   `[x] DONE`: The task is complete.
-   `[-] SKIPPED`: The task is no longer relevant or has been superseded.

---

## Phase 1: Correctness and Logic Fixes

**Goal**: Fix the premature script termination bug and the inefficient exploration of empty branches. This is the highest priority.

| Task ID | Description                                                                                                                                                                                                                                                                                                                                                     | Status    |
| :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| **1.1** | **Streamline `ProgressTracker`**: In `src/utils/progress_tracker.py`, remove all logic related to the legacy `systematic_request_tracker.csv`. This includes removing the `_rewrite_tracker_file` and `_initialize_tracker_file` methods, and the `tracker_path` and `tracker_fieldnames` attributes from the `__init__` method. | `[x] DONE` |
| **1.2** | **Simplify `log_check` Method**: In `src/utils/progress_tracker.py`, modify the `log_check` method to no longer accept a `status` argument. The status should be determined internally by the `_process_event_row` method based on `is_workable` and `total_profiles`, making the tracker the single source of truth for status logic.       | `[x] DONE` |
| **1.3** | **Fix Restart Logic in `process_layer`**: In `run_systematic_profile_search.py`, overhaul the `if progress:` block to correctly handle all distinct states (`COMPLETED`, `IN_PROGRESS`, `PENDING`, `SKIPPED_TOO_LARGE`, `SKIPPED_NO_RESULT`). This ensures the correct action (submit, descend, or prune) is taken for each state on restart. | `[x] DONE` |

---

## Phase 2: Performance Refactoring - Decoupled I/O Architecture

**Goal**: Re-architect the script to use a multi-queue system, isolating network operations from disk I/O to dramatically improve throughput.

| Task ID | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Status    |
| :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| **2.1** | **Introduce Queues and Threads**: In `run_systematic_profile_search.py`, import `queue` and `threading`. In `main()`, initialize three `queue.Queue` objects: `work_queue`, `results_queue`, and `progress_queue`.                                                                                                                                                                                                                                                                                                              | `[x] DONE` |
| **2.2** | **Create File Writer Worker**: In `main()`, define a `file_writer_worker` that gets `(response_data, params)` tuples from `results_queue` and saves them using `file_utils.save_json_response`. The loop must terminate on a `None` sentinel. Start this worker in a dedicated background `threading.Thread`.                                                                                                                                                                                                                | `[x] DONE` |
| **2.3** | **Create Progress Logger Worker**: In `main()`, define a `progress_logger_worker` that gets `(event_type, params, data)` tuples from `progress_queue` and calls the appropriate `ProgressTracker` method. The loop must terminate on a `None` sentinel. Start this worker in a dedicated background `threading.Thread`.                                                                                                                                                                                                           | `[x] DONE` |
| **2.4** | **Refactor `process_layer` as Producer**: Modify `process_layer`'s signature to remove the `executor` argument. When a workable query is found, it will now put a `(params, total_profiles)` tuple onto the `work_queue`. This function's sole responsibility becomes *finding* work.                                                                                                                                                                                                                                             | `[x] DONE` |
| **2.5** | **Create `downloader_worker` as Consumer**: Create a new `downloader_worker` function that will be the target for the `ThreadPoolExecutor`. This function will run a `while True` loop, getting jobs from the `work_queue`. Inside the loop, it will call a refactored `mass_request_pages` function. The loop must terminate when it receives a `None` sentinel.                                                                                                                                                               | `[x] DONE` |
| **2.6** | **Refactor `mass_request_pages`**: Simplify `mass_request_pages` to process a single work item `(params, total_profiles)`. For each API response, it will put `(response_data, params)` on the `results_queue`. For each page event, it will put `(event_type, params, data)` on the `progress_queue`. It will no longer have a loop.                                                                                                                                                                                              | `[x] DONE` |
| **2.7** | **Adapt `main` for New Architecture**: The `ThreadPoolExecutor` in `main()` will now target the `downloader_worker` function. The main thread will call `process_layer`, then call `work_queue.join()` to wait for all items to be processed. Finally, it will put a `None` sentinel *for each worker thread* onto `work_queue` and a single `None` sentinel on the other queues to gracefully shut down all background threads. | `[x] DONE` |

---

## Phase 3: Documentation and Cleanup

**Goal**: Ensure the project's documentation reflects the new, improved architecture.

| Task ID | Description                                                                                                                                                                              | Status    |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| **3.1** | **Update `systematic_data_extraction.md`**: Edit the documentation to describe the new queue-based architecture, the corrected logic, and remove any references to the old `request_tracker.csv`. | `[x] DONE` |
| **3.2** | **Finalize this Plan**: Update this document to mark all tasks as `[x] DONE`.                                                                                                                | `[x] DONE` |
