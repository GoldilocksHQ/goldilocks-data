---
title: "Systematic Neuron360 Data Extraction"
created_at: "2025-06-14"
updated_at: "2025-06-15"
---

# Systematic Neuron360 Data Extraction

## 1. Objective

The primary goal of this exercise is to systematically query and download all available profile data from the Neuron360 API for profiles located in the United Kingdom. The process is designed to be exhaustive, resilient, and auditable by iterating through a complex hierarchy of search parameters and handling API limitations.

## 2. Core Logic & Parameter Hierarchy

The extraction process is governed by a hierarchical logic that progressively narrows down the search query until the number of results is manageable within the Neuron360 API's limits (a maximum of 10,000 profiles per query). The script will start with a broad query and add more specific filters layer by layer if the result set is too large.

The parameters are categorized into three groups:

-   **Static Parameter**: Fixed throughout all queries.
-   **Moving Parameters**: Iterated in a specific order to slice the data.
-   **Toggle Parameters**: Used as final filters to further segment the data.

The hierarchy is as follows:

1.  **Static - Country**: `United Kingdom`
2.  **Layer A - Last Modified Date**: Monthly intervals, from May 2025 back to December 2024.
    -   Example Range 1: `since 2025-05-01` and `before 2025-05-31`
    -   Example Range 2: `since 2025-04-01` and `before 2025-04-30`
    -   ...and so on.
3.  **Layer B - Completion Score**: Five non-overlapping ranges.
    -   Range 1: `> 0.4` and `< 0.45`
    -   Range 2: `> 0.45` and `< 0.50`
    -   Range 3: `> 0.50` and `< 0.55`
    -   Range 4: `> 0.55` and `< 0.60`
    -   Range 5: `> 0.6` and `< 1.0`
4.  **Layer C - Job Seniority**: Iterate through all values in the `JobSeniority` enum.
5.  **Layer D - Job Function**: Iterate through all values in the `JobFunction` enum.
6.  **Layer E - Skill Category**: Iterate through all values in the `SkillCategory` enum.
7.  **Layer F - Skill Subcategory**: For each Skill Category, iterate through its associated subcategories. The relationship is defined in `src/enums/neuron360/skills.py`.
8.  **Layer G - City (London)**: Two options.
    -   Option 1: `is one of ["London"]`
    -   Option 2: `is not one of ["London"]`
9.  **Layer H - Profile Tags**: Two options.
    -   Option 1: `is one of ["Profile Has Phone", "Profile Has Address", "Profile Has Email"]`
    -   Option 2: `is not one of ["Profile Has Phone", "Profile Has Address", "Profile Has Email"]`

This hierarchical logic is implemented in the `ParameterProvider` class (`src/utils/parameter_provider.py`), which recursively generates all possible search parameter combinations. It interacts with the `ProgressTracker` to skip combinations that have already been successfully processed in previous runs.

## 3. Concurrent Execution & Architecture

The script uses a multi-threaded, queue-based architecture to maximize performance by decoupling network I/O from disk I/O. It consists of four main components:

-   **Producer (Main Thread)**: A single main thread is responsible for exploring the parameter hierarchy via the recursive `process_layer` function. When it discovers a "workable" query, it does not perform the download itself. Instead, it places the parameter set and its total profile count onto the `work_queue`.
-   **Downloader Workers (Thread Pool)**: A pool of worker threads (number configurable via `--threads`) are the consumers of the `work_queue`. Each worker pulls a parameter set, executes the `mass_request_pages` function to download all pages, and places the results and progress updates onto two separate queues.
-   **File Writer (Dedicated Thread)**: A single, dedicated thread consumes from the `results_queue`. Its only job is to write the JSON response data to disk. This isolates all file-writing I/O, preventing it from blocking the high-volume downloader threads.
-   **Progress Logger (Dedicated Thread)**: A single, dedicated thread consumes from the `progress_queue`. Its only job is to log events to the `ProgressTracker`, ensuring that updates to the ledger file are handled efficiently and in a thread-safe manner without slowing down the downloaders.

This behavior can be configured with the following command-line arguments:

-   `--threads`: (Optional) Specifies the number of concurrent downloader worker threads. The default value is `5`. Increasing this number can significantly improve download speed.
-   `--dry-run`: (Optional) If this flag is present, the script will perform the entire parameter exploration process but will not place any items on the work queue. This is useful for validating the query logic without making any API calls.

## 4. Execution Flow

The script operates using a recursive producer and multiple concurrent consumers.

1.  **Initialize**: The script starts all worker threads (downloaders, writer, logger), which are idle, waiting for items on their respective queues.
2.  **Produce Work**: The main thread begins the recursive `process_layer` exploration. It starts with the static `country` parameter and descends through the hierarchy.
3.  **Check Total Results**: A single API request is made with the current set of parameters (`page_size: 1`) to fetch the `counts.profiles_total_results`.
4.  **Decision Point**:
    -   **If `profiles_total_results` < 10,000 (and > 0)**:
        -   The query is "workable."
        -   The `(parameters, total_profiles)` are placed on the `work_queue`.
        -   The script then moves to the *next* parameter value in the *current* layer.
    -   **If `profiles_total_results` >= 10,000**:
        -   The query is too broad. The script descends to the next layer in the hierarchy and repeats the **Check Total Results** step with the newly refined query.
    -   **If `profiles_total_results` == 0**:
        -   The query is empty. This branch is pruned, and the script moves to the next parameter value in the current layer.
5.  **Consume Work**: As soon as a work item appears on the `work_queue`, an idle downloader thread picks it up and begins fetching all pages for that query.
6.  **Process and Distribute**: For each page downloaded, the downloader thread places the JSON response on the `results_queue` and a page completion message on the `progress_queue`.
7.  **Write and Log**: The file writer and progress logger threads work concurrently in the background, saving files and updating the ledger.
8.  **Completion**: The main thread finishes exploring the hierarchy and waits for all queues to be empty. It then signals the worker threads to exit, and the script finishes.

## 5. Progress Tracking

A robust, append-only **Ledger CSV** (`goldilocks-data/data/systematic_request_ledgers/`) is the source of truth for tracking progress. This allows the script to be stopped and resumed without losing its place.

The ledger stores events (`CHECK`, `PAGE_UPDATE`, `COMPLETED`, `FAILED`) and reconstructs the full state of the system on startup, ensuring that already-completed work is skipped.

## 6. Skills Enum Enhancement

The `src/enums/neuron360/skills.py` file has been updated to include the complete and correct taxonomy of skills as defined by the Neuron360 documentation. This includes:
-   A comprehensive `SkillCategory` enum.
-   A comprehensive `SkillSubCategory` enum.
-   A `SKILL_HIERARCHY` dictionary that maps each `SkillCategory` to a list of its corresponding `SkillSubCategory` members, which is crucial for the hierarchical iteration (Layer E -> Layer F).

## 7. Error Handling and Logging

To ensure the extraction process is robust and resilient, several error handling mechanisms have been implemented:

-   **API Retries**: The core `Neuron360Service` includes a retry mechanism with exponential backoff. It automatically re-attempts requests that fail with a 5xx server error.
-   **Failed Request Logging**: Any API request that ultimately fails (after all retries) is logged to a dedicated file: `logs/failed_requests.log`. This log contains the full request parameters and the error response, allowing for manual inspection and re-processing at a later time.

## 8. Testing

The script includes features to facilitate testing and validation:

-   **Dry Run Mode**: The `--dry-run` command-line argument allows the script to execute its entire parameter generation and decision-making logic without making any actual data-downloading API calls.
-   **Unit Tests**: The project includes unit tests for key components. Mocks are used to isolate services and validate their behavior independently.
