# Goldilocks Data

This project is a data integration service designed to process data from a JSON response, validate it against a set of Pydantic models, and persist it into a Supabase database. It is structured to handle different data schemas, specifically for "people" and "organisation" entities, with a clear separation of concerns between business logic, database services, and data models.

## Table of Contents

- [Project Structure](#project-structure)
- [System Design](#system-design)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running Tests](#running-tests)

## Project Structure

The project follows a standard Python application structure:

```
goldilocks-data/
├── .env.example
├── README.md
├── requirements.txt
├── setup.py
├── main.py
├── run_profile_search.py
├── data/
│   └── .gitkeep
├── data_schema/
│   └── example/
│       ├── search_profile_response_full_eg1.json
│       ├── search_profile_response_full_eg2.json
│       └── search_profile_response_full_eg3.json
├── design_docs/
│   └── system_design.md
├── src/
│   ├── enums/
│   │   └── neuron360/
│   │       ├── __init__.py
│   │       ├── contact_tags.py
│   │       ├── job_functions.py
│   │       ├── job_seniorities.py
│   │       ├── profile_tags.py
│   │       ├── resume_tags.py
│   │       └── skills.py
│   ├── models/
│   │   ├── people/
│   │   └── organisation/
│   ├── services/
│   │   ├── base_service.py
│   │   ├── neuron360_service.py
│   │   ├── people_services.py
│   │   └── organisation_services.py
│   ├── managers/
│   │   ├── base_manager.py
│   │   ├── people_manager.py
│   │   ├── organisation_manager.py
│   │   └── profile_search_manager.py
│   └── utils/
│       ├── config.py
│       ├── logging.py
│       └── validators.py
├── tests/
│   ├── unit/
│   └── integration/
└── sql/
    └── table_creation_query/
```

- **`main.py`**: The main entry point to run the data processing pipeline.
- **`run_profile_search.py`**: The entry point to perform a live search against the Neuron360 Profile Search API.
- **`data/`**: Contains files related to data processing.
- **`data_schema/`**: Contains example JSON data for testing.
- **`design_docs/`**: Contains detailed documentation on the system architecture.
- **`src/`**: The source code for the application.
  - **`enums/`**: Contains files related to Neuron360.
  - **`models/`**: Pydantic models for data validation and structure.
  - **`services/`**: Handles database interactions. Each service has a dedicated client for its specific schema (`people` or `organisation`).
  - **`managers/`**: Orchestrates the data flow and business logic.
  - **`utils/`**: Shared utilities for configuration, logging, etc.
- **`tests/`**: Contains all the tests for the project.
- **`sql/`**: SQL scripts for database schema creation.

## System Design

For a detailed explanation of the project's architecture, components, and data flow, please see the [System Design Document](./design_docs/system_design.md).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd goldilocks-data
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application uses a `.env` file for configuration.

1.  **Create a `.env` file** by copying the example:
    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file** with your Supabase and Neuron360 credentials:
    ```
    SUPABASE_URL="your-supabase-url"
    SUPABASE_KEY="your-supabase-key"
    NEURON360_API_KEY="your-neuron360-api-key"
    NEURON360_API_URL="https://api.neuron360.io"
    ```

## Usage

The project has two main entry points:

### 1. Ingesting from a File

To run the data processing pipeline with the default example data from a local file, execute the `main.py` script:

```bash
python main.py
```

This will:
1.  Load the example data from `data_schema/example/search_profile_response_full_eg1.json`.
2.  Initialize the `PeopleManager` and `OrganisationManager`.
3.  Process the data, validate it, and persist it to your Supabase instance.

### 2. Searching the Live API

To perform a live search against the Neuron360 Profile Search API, execute the `run_profile_search.py` script:

```bash
python run_profile_search.py
```

This will:
1.  Load the sample search query defined in the script.
2.  Initialize the `ProfileSearchManager`.
3.  Execute the search, save the response to `goldilocks-data/data/neuron360/profile_search/`, and log the results.
The script can be easily modified to change the search parameters or perform paginated searches.

## Running Tests

The project uses `pytest` for testing. To run the test suite:

```bash
pytest
```

This will discover and run all tests in the `tests/` directory.
