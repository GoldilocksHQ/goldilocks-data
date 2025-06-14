---
title: "Systematic Neuron360 Data Extraction"
created_at: "2025-06-14"
updated_at: "2025-06-14"
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

## 3. Execution Flow

The script will operate using a recursive or deeply nested loop structure that follows the parameter hierarchy.

1.  **Initialize Query**: The script starts with the static `country` parameter and the first value from the highest-level moving parameter (Layer A: `last_modified_date`).

2.  **Check Total Results**: A single API request is made with the current set of parameters (`page_size: 1`, `page_number: 1`) to fetch the `counts.profiles_total_results`.

3.  **Decision Point**:
    -   **If `profiles_total_results` < 10,000**:
        -   The query is considered "workable."
        -   The script enters **Mass Request Mode**.
        -   It calculates the total number of pages and iterates from page 1 to the last page, sending a request for each.
        -   Each successful response is saved as a separate JSON file.
        -   The progress for this parameter combination is logged to the tracking CSV (see Section 5).
        -   The script then moves to the *next* parameter value in the *current* layer (e.g., the next date range).
    -   **If `profiles_total_results` >= 10,000**:
        -   The query is too broad.
        -   The script descends to the next layer in the hierarchy (e.g., from Layer A to Layer B).
        -   It adds the *first* parameter value from this new, deeper layer to the query.
        -   It repeats the **Check Total Results** step with the newly refined query.

4.  **Bottom of Hierarchy**: If the script reaches the final layer (Layer H) and the total results are still >= 10,000, it will proceed with the **Mass Request Mode** for that query, accepting that it will only be able to retrieve the first 10,000 of the available profiles.

## 4. Rate Limiting

To avoid overwhelming the Neuron360 API, a rate limit will be strictly enforced. The script will ensure that no more than 1,000 requests are sent per minute. This will be achieved by introducing a small delay (e.g., 60ms) after each API call.

## 5. Progress Tracking

A CSV file (`data/request_tracker.csv`) will be used to log the state of the extraction process. This allows for monitoring and enables the script to be stopped and resumed without losing progress.

The CSV will have the following columns:

-   `timestamp`: When the query was executed.
-   `parameters_json`: A JSON string representing the exact `parameters` payload used for the query.
-   `total_profiles`: The value of `profiles_total_results` for the query.
-   `status`: The outcome of the query (e.g., `COMPLETED`, `IN_PROGRESS`, `SKIPPED_TOO_LARGE`).
-   `last_completed_page`: The last page number successfully downloaded. For completed queries, this will equal the total number of pages.
-   `error_message`: Any error message encountered during processing.

## 6. Skills Enum Enhancement

The `src/enums/neuron360/skills.py` file will be updated to include the complete and correct taxonomy of skills as defined by the Neuron360 documentation. This includes:
-   A comprehensive `SkillCategory` enum.
-   A comprehensive `SkillSubCategory` enum.
-   A dictionary mapping each `SkillCategory` to a list of its corresponding `SkillSubCategory` members, which is crucial for the hierarchical iteration (Layer E -> Layer F).
