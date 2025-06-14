---
title: Implementation Plan - Neuron360 Profile Search API Integration
created_at: 2025-06-14
updated_at: 2025-06-14
---

# Implementation Plan: Neuron360 Profile Search API

## 1. Context and Objectives

This document outlines the implementation plan for integrating the Neuron360 Profile Search API into the Goldilocks data platform. The primary objective is to create a robust and scalable client to query the Neuron360 database for professional profiles based on a wide range of criteria, such as job titles, skills, location, and more.

This integration will enable the platform to fetch targeted profile data, which can then be used for analysis, enrichment, or further processing within the existing data pipeline.

The implementation will follow the existing architectural pattern of Managers and Services to ensure separation of concerns and maintainability.

## 2. Key Information & Design Decisions

### 2.1. API Details

-   **Endpoint**: `POST https://api.neuron360.io/profile/search`
-   **Authentication**: Via an `x-api-key` header. The key is stored in the `.env` file under the variable `NEURON360_API_KEY`.
-   **Core Request Body Structure**: The API expects a JSON payload with two main keys:
    -   `reveal_all_data` (boolean): Controls whether the full or partial profile is returned. **This will be set to `false` by default in our implementation.**
    -   `parameters` (object): A dictionary containing the search filters.
        -   An **AND** operator is applied between different parameters (e.g., `countries` AND `job_titles`).
        -   An **OR** operator is applied between values within the same parameter (e.g., "london" OR "manchester").
-   **Reference Documentation**:
    -   [API Reference](https://docs.neuron360.io/reference/post_profile-search)
    -   [Request Parameters](https://docs.neuron360.io/docs/profile-search-api-parameters)
    -   [Python Example](https://docs.neuron360.io/docs/profile-search-api-python)

### 2.2. Proposed Architecture & Folder Structure

To align with the project's existing design, we will introduce the following new components:

-   **Configuration (`src/utils/config.py`)**:
    -   The existing config loader will be updated to read `NEURON360_API_KEY` and `NEURON360_API_URL` from the `.env` file.

-   **Enums/Constants (`src/enums/neuron360/`)**:
    -   A new directory, `src/enums/neuron360`, will be created to house all enums related to the Neuron360 API.
    -   Each enum will be in its own file for easier maintenance (e.g., `src/enums/neuron360/profile_tags.py`). This promotes code readability, maintainability, and type safety.

-   **API Service Layer (`src/services/`)**:
    -   **`src/services/neuron360_service.py`**: A new service dedicated to handling all communication with the Neuron360 API.
        -   It will be responsible for constructing the HTTP headers, making the `POST` request, and handling low-level responses and errors (e.g., HTTP status codes, connection errors).

-   **Manager/Business Logic Layer (`src/managers/`)**:
    -   **`src/managers/profile_search_manager.py`**: This new manager will act as the high-level interface for conducting profile searches.
        -   It will abstract the complexity of building the API query.
        -   It will expose a clear method, like `search_profiles()`, that accepts user-friendly parameters (leveraging the enums).
        -   It will be responsible for orchestrating calls to the `Neuron360Service`.
        -   It will handle the logic for saving API responses to the file system.

-   **Data Storage (`data/`)**:
    -   API responses will be stored in a new, structured directory: **`data/neuron360/profile_search/`**.
    -   Files will be named with a timestamp to avoid collisions and provide a clear history (e.g., `response_2025-06-14_12-30-00.json`).

-   **Execution Script (`/`)**:
    -   A new script, **`run_profile_search.py`**, will be created at the project root (`goldilocks-data/`) to demonstrate and execute a search using the new manager.

## 3. Implementation Phases & Tasks

### Legend

-   `[TODO]` - Task has not started.
-   `[WIP]` - Task is in progress.
-   `[DONE]` - Task is complete.
-   `[BLOCKED]` - Task is blocked by another task.

---

### Phase 1: Foundation and Configuration

This phase focuses on setting up the necessary configuration and data structures.

| Task ID | Description                                                                                                                              | Status   |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| P1-T1   | Set up environment variables (`NEURON360_API_KEY`, `NEURON360_API_URL`) in the `.env` file.                                                 | `[DONE]` |
| P1-T2   | Update the `Config` class in `src/utils/config.py` to load the new environment variables.                                                  | `[DONE]` |
| P1-T3   | Create the directory `src/enums/neuron360/` and add an `__init__.py` file.                                                                | `[DONE]` |
| P1-T4   | Create `src/enums/neuron360/profile_tags.py` with `ProfileTag` enum. ([Ref](https://docs.neuron360.io/docs/profile-tags))                   | `[DONE]` |
| P1-T5   | Create `src/enums/neuron360/resume_tags.py` with `ResumeTag` enum. ([Ref](https://docs.neuron360.io/docs/resume-tags))                     | `[DONE]` |
| P1-T6   | Create `src/enums/neuron360/contact_tags.py` with `ContactTag` enum. ([Ref](https://docs.neuron360.io/docs/contact-tags))                   | `[DONE]` |
| P1-T7   | Create `src/enums/neuron360/job_functions.py` with `JobFunction` enum. ([Ref](https://docs.neuron360.io/docs/job-functions))               | `[DONE]` |
| P1-T8   | Create `src/enums/neuron360/job_seniorities.py` with `JobSeniority` enum. ([Ref](https://docs.neuron360.io/docs/job-seniorities))           | `[DONE]` |
| P1-T9   | Create `src/enums/neuron360/skills.py` with `SkillCategory` and `SkillSubCategory` enums. ([Ref](https://docs.neuron360.io/docs/enhanced-skills-taxonomy)) | `[DONE]` |

---

### Phase 2: API Service Layer

This phase focuses on building the direct client for the Neuron360 API.

| Task ID | Description                                                                                                                                                            | Status   |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| `P2-T1` | Create the `src/services/neuron360_service.py` file.                                                                                                                   | `[DONE]` |
| `P2-T2` | Implement the `Neuron360Service` class with an `__init__` method that retrieves the API key and URL from the config.                                                    | `[DONE]` |
| `P2-T3` | Implement a `search_profiles(payload: dict) -> dict` method in `Neuron360Service`.                                                                                      | `[DONE]` |
| `P2-T4` | Inside `search_profiles`, implement the `requests.post` call with the correct URL, headers (`x-api-key`, `Content-Type`), and JSON payload.                             | `[DONE]` |
| `P2-T5` | Add robust error handling in the service for non-200 status codes, request exceptions (e.g., timeouts), and invalid JSON responses. Raise custom exceptions if needed. | `[DONE]` |

---

### Phase 3: Manager and Business Logic Layer

This phase focuses on creating the high-level manager to orchestrate searches.

| Task ID   | Description                                                                                                                                                                                                           | Status   |
| :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| `P3-T1`   | Create the `src/managers/profile_search_manager.py` file.                                                                                                                                                             | `[DONE]` |
| `P3-T2`   | Implement the `ProfileSearchManager` class, initializing the `Neuron360Service` in its constructor.                                                                                                                   | `[DONE]` |
| `P3-T3`   | Design and implement the main `search()` method. It should accept filter parameters (`job_titles`, etc.) and pagination parameters (`page_number`, `page_size`).                                                       | `[DONE]` |
| `P3-T4`   | Implement the logic within `search()` to build the nested `parameters` dictionary required by the Neuron360 API, using the provided arguments.                                                                         | `[DONE]` |
| `P3-T5`   | Ensure the `search()` method correctly handles enums, converting them to their string values for the API payload.                                                                                                     | `[DONE]` |
| `P3-T6`   | Ensure the `search()` method sets `reveal_all_data: false` by default in the payload.                                                                                                                                  | `[DONE]` |
| `P3-T7`   | Implement a private method `_save_response_to_file(response: dict)` within the manager.                                                                                                                               | `[DONE]` |
| `P3-T8`   | The `_save_response_to_file` method should create the `data/neuron360/profile_search/` directory if it doesn't exist and save the response as a timestamped JSON file.                                                | `[DONE]` |
| `P3-T9`   | Call the `_save_response_to_file` method within the `search()` method after a successful API call.                                                                                                                    | `[DONE]` |
| `P3-T10`  | Implement pagination logic in the `search()` method. It should enforce API limits (max `page_size`: 100, max `page_number`: 100). (Ref: `pagination` object in `search_profiles_response_full.json`)                  | `[DONE]` |
| `P3-T11`  | Implement a public method `get_total_profiles(response: dict) -> int` in the manager to extract the `profiles_total_results` count from a raw API response. (Ref: `counts.profiles_total_results` in `search_profiles_response_full.json`) | `[DONE]` |

---

### Phase 4: Integration and Execution

This phase focuses on creating an entry point to run the search and test the full implementation.

| Task ID | Description                                                                                                                        | Status   |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------- | :------- |
| `P4-T1` | Create the `run_profile_search.py` script in the `goldilocks-data/` root directory.                                                  | `[DONE]` |
| `P4-T2` | In `run_profile_search.py`, import and instantiate the `ProfileSearchManager`.                                                       | `[DONE]` |
| `P4-T3` | Create a `main()` function in the script that defines a sample search query (e.g., search for "Software Engineer" in "Canada").      | `[DONE]` |
| `P4-T4` | Call the `manager.search()` method with the sample query and print a confirmation message indicating where the response was saved.   | `[DONE]` |
| `P4-T5` | Perform a final end-to-end test run of `run_profile_search.py` to ensure the entire flow works and the file is saved correctly.      | `[DONE]` |
