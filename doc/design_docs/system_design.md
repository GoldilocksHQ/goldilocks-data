---
title: Goldilocks Data - System Design
created_at: 2025-06-14
updated_at: 2025-06-14
---

# Goldilocks Data - System Design

## 1. Overview

The Goldilocks Data project is a data processing pipeline designed to ingest complex, nested JSON data, validate it, transform it, and persist it into a multi-schema Supabase database. The primary goal is to create a structured and relational representation of professional profiles (`people` schema) and their associated work histories (`organisation` schema) from a semi-structured source.

The system is architected to be robust, scalable, and maintainable, with a clear separation of concerns between data validation, business logic, and database interaction.

## 2. Core Components

The application is built around three main layers: **Managers**, **Services**, and **Models**.

### 2.1. Models (`src/models/`)

-   **Purpose**: Define the canonical data structures for all entities in the system. Some nested objects from the source data (like web addresses for a person's education) are flattened and embedded directly into their parent model.
-   **Technology**: Pydantic `BaseModel`.
-   **Functionality**:
    -   Each table in the Supabase database has a corresponding Pydantic model (e.g., `people.identities` maps to `people.Identity`).
    -   Models provide robust data validation, type enforcement, and serialization/deserialization capabilities.
    -   They serve as the single source of truth for the data schema within the application code.

### 2.2. Services (`src/services/`)

-   **Purpose**: Abstract all direct database or external API interactions. This layer is the only part of the application that should communicate with external systems like Supabase or Neuron360.
-   **Key File**: `base_service.py`, `neuron360_service.py`
-   **Functionality**:
    -   **`BaseService`**: A generic class providing standard CRUD (Create, Read, Update, Delete) and `upsert` operations for the Supabase database.
    -   **`Neuron360Service`**: A dedicated client for the Neuron360 Profile Search API. It handles request construction, authentication via API key, and low-level error handling (e.g., HTTP status codes, timeouts).
    -   **Schema-Specific Clients**: The `BaseService` is uniquely configured to handle Supabase's multi-schema environment. When a service is instantiated (e.g., `PeopleService`), it specifies a table name like `"people.identities"`. The `BaseService` constructor parses the schema (`people`) from the table name and creates a dedicated Supabase client instance using `ClientOptions(schema=schema)`. This ensures all subsequent operations for that service instance are correctly routed to the appropriate schema.
    -   **Specialized Services**: Most tables have their own service class (e.g., `people_services.IdentityService`, `organisation_services.OfficeService`) that inherits from `BaseService`, providing a clean, table-specific API to the rest of the application. This modularity allows business logic components to request data without needing to know about the underlying database implementation.
    -   **Serialization Workaround**: The `create` and `upsert` methods in `BaseService` include a specific workaround for a known issue with `supabase-py` and Pydantic models containing UUIDs. Data is first serialized to a JSON string using `model_dump_json()` and then loaded back into a dictionary using `json.loads()`. This ensures that UUIDs and other complex types are correctly formatted before being sent to the database.

### 2.3. Managers (`src/managers/`)

-   **Purpose**: Orchestrate the entire data processing workflow. This layer contains all the business logic for transforming the raw JSON data into the structured format defined by the Pydantic models.
-   **Key Files**: `people_manager.py`, `organisation_manager.py`, `profile_search_manager.py`
-   **Functionality**:
    -   **`PeopleManager`**: The primary orchestrator for ingesting profile data from a file. It iterates through each person's record from the source data and manages the entire lifecycle of processing that person and all their related sub-records (profile, experiences, education, etc.).
    -   **`OrganisationManager`**: A specialized manager responsible for processing company and office data. It is instantiated and owned by the `PeopleManager`.
    -   **`ProfileSearchManager`**: A high-level interface for conducting live searches against the Neuron360 API. It abstracts the complexity of building the query payload, handles pagination, orchestrates calls to the `Neuron360Service`, and saves the results.
    -   **Inter-Manager Communication**: The `PeopleManager` delegates responsibility for company data. When processing a person's work experience, it calls `org_manager.process_organisation_data()`, passing the relevant experience data. This design ensures a clean separation of concerns, where the `PeopleManager` doesn't need to know the details of how organizations are processed.
    -   **Data Transformation**: Managers are responsible for flattening nested JSON objects, renaming keys, casting data types (e.g., string to date), and structuring data to match the Pydantic models before passing it to the services layer for persistence.
    -   **Duplicate Handling**: The `OrganisationManager` implements logic to prevent duplicate entries by checking if an organization with a given `company_id` already exists before attempting to create a new one. The `PeopleManager` does the same for people records using the `neuron360_profile_id`.

## 3. Data Flow

The project supports two primary data flows: file-based ingestion and live API searching.

### 3.1. File-Based Ingestion (`main.py`)

The data processing pipeline is initiated from `main.py` and follows a clear, sequential flow:

1.  **Initialization**: `main.py` loads the source JSON file.
2.  **Manager Instantiation**: An `OrganisationManager` instance is created, which is then passed to the constructor of the `PeopleManager`.
3.  **Person Iteration**: `main.py` loops through each person record in the `results` array of the JSON data and calls `people_manager.process_person_data()` for each one.
4.  **Person Processing**:
    -   The `PeopleManager` receives a single person record.
    -   It first creates the primary `people.identities` record.
    -   It then processes all profile-level data (address, emails, social links, etc.) and creates the corresponding records in the `people` schema.
5.  **Experience and Organisation Processing**:
    -   The `PeopleManager` iterates through the list of `experiences` for the person.
    -   For **each experience**, it first calls `self.org_manager.process_organisation_data()`, passing the experience dictionary.
    -   The `OrganisationManager` checks if the organization (identified by `company_id`) already exists.
        -   If it exists, the manager skips creation and returns.
        -   If it's new, the manager creates the primary `organisation.identities` record, followed by all its related sub-records (web addresses, employees, industries, etc.). It then proceeds to process any associated `office` data in the same manner.
    -   After the `OrganisationManager` has finished, control returns to the `PeopleManager`, which then creates the `people.experiences` record, linking it to the person. It proceeds to create all experience-related sub-records (job functions, seniority, etc.).
6.  **Resume Item Processing**: After processing all experiences, the `PeopleManager` continues to process other top-level resume items like `educations`, `certifications`, `patents`, etc., creating records in the appropriate `people` schema tables.
7.  **Completion**: The process repeats for the next person until all records from the source file have been processed.

### 3.2. Live API Search (`run_profile_search.py`)

1.  **Initialization**: `run_profile_search.py` instantiates the `ProfileSearchManager`.
2.  **Search Execution**: The script defines a search query (either simple key-value pairs or a complex, nested dictionary) and calls the `manager.search()` method.
3.  **API Call**: The `ProfileSearchManager` builds the final JSON payload, including pagination details and the `reveal_all_data` flag, and passes it to the `Neuron360Service`.
4.  **Response Handling**: The `Neuron360Service` makes the `POST` request to the Neuron360 API. Upon receiving a successful response, the `ProfileSearchManager` saves the data to a timestamped JSON file in `goldilocks-data/data/neuron360/profile_search/`.
5.  **Pagination**: The `run_profile_search.py` script can be configured to loop through multiple pages of results, making consecutive calls until all data is fetched.

## 4. Configuration

-   The application relies on a `.env` file at the root of the project (`goldilocks-data/`) for all environment-specific settings.
-   Key variables include `SUPABASE_URL`, `SUPABASE_KEY`, `NEURON360_API_KEY`, and `NEURON360_API_URL`.
-   Configuration is loaded into a singleton `config` object via `src/utils/config.py` for easy access throughout the application.
