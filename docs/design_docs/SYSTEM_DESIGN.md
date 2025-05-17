# Goldilocks-Data: System Design Document

## 1. Introduction

This document outlines the system design for the `goldilocks-data` project. The initial goal of this project is to create a local dataset by fetching company information from the Neuron360 API, enriching this data with industry tags and business type information using LLMs (Gemini and DeepSeek), and then storing the combined data locally.

This project is designed to be standalone and prioritizes clarity, modularity, and ease of switching between different LLM vendors.

## 2. High-Level Flow

The data processing pipeline involves the following key stages:

1.  **Configuration Loading:** Initialize the application by loading necessary configurations such as API keys, model names, base URLs, and operational parameters (e.g., concurrency limits) from environment variables.
2.  **Data Fetching (Neuron360):**
    *   A dedicated service constructs a request for the Neuron360 `/company/search` API endpoint.
    *   Initial parameters: `reveal_all_data = false`, `industries_names = "Computers, peripherals, and software"`, `countries = "United Kingdom"`, `tags = ["Has URL"]`.
    *   The service aims to fetch 100 company records, handling pagination as required by the Neuron360 API (using `page_number` and `page_size`, with `page_size` up to 100).
    *   A specialized API client executes the request and retrieves the raw company data.
3.  **Initial Storage & Preparation:**
    *   The list of raw company profiles fetched from Neuron360 is saved to a local JSON file (`data/companies/neuron360_company_profiles.json`).
    *   For each company record, specific relevant fields (as defined by `company_tags_agent_required_info.json`) are extracted. Empty or null fields are excluded to provide clean, concise input for the LLM.
4.  **Data Enrichment (LLM):**
    *   This stage is performed concurrently for each company profile to improve throughput.
    *   A `CompanyTagsAgent` prepares the extracted company information and crafts a detailed prompt.
    *   The appropriate LLM client (Gemini or DeepSeek, chosen via configuration) is invoked.
    *   The LLM is instructed to act as an expert company investigator and return `industry_tags` and `business_types` in a structured JSON format.
    *   The number of concurrent LLM requests is managed by a configurable semaphore.
5.  **Final Storage:**
    *   The enriched data, combining the original Neuron360 profile with the LLM-generated tags and metadata about the enrichment process (LLM vendor used, status), is compiled.
    *   This final list of enriched company objects is saved to a local JSON file (`data/companies/company_tags.json`).

## 3. Key Components Design

### 3.1. `main.py`
*   **Purpose:** Orchestrator for the entire data processing pipeline.
*   **Logic:**
    *   Initializes configurations.
    *   Instantiates and uses the `Neuron360APIClient` for data fetching.
    *   Loads fetched data and prepares for enrichment.
    *   Uses the `LLMFactory` to get the configured LLM client.
    *   Instantiates the `CompanyTagsAgent`.
    *   Manages asynchronous and concurrent processing of company records for LLM enrichment using `asyncio` and `asyncio.Semaphore`.
    *   Collects enriched data and saves it.
    *   Includes basic logging for operations and errors.

### 3.2. `config.py`
*   **Purpose:** Centralized configuration management.
*   **Logic:**
    *   Uses `python-dotenv` to load variables from a `.env` file.
    *   Provides access to:
        *   `NEURON360_API_KEY`, `NEURON360_BASE_URL`.
        *   `LLM_VENDOR` (string: "gemini" or "deepseek").
        *   `GEMINI_API_KEY`, `GEMINI_MODEL_NAME` (e.g., "gemini-1.5-flash-latest").
        *   `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL_NAME` (e.g., "deepseek-chat"), `DEEPSEEK_BASE_URL`.
        *   `MAX_CONCURRENT_LLM_REQUESTS` (integer for semaphore).
        *   `LLM_REQUEST_DELAY_SECONDS` (float, optional delay between individual LLM calls within the semaphore).
*   **Design Decision:** Keeps all sensitive and environment-specific settings externalized from the code, promoting security and flexibility.

### 3.3. `neuron360_service/client.py` (`Neuron360APIClient`)
*   **Purpose:** Handles all direct communication with the Neuron360 API.
*   **Design:**
    *   Constructor: `__init__(self, api_key: str, base_url: str)`.
    *   Core Method: `async search_companies(self, search_params: dict, num_records_to_fetch: int = 100) -> list[dict]`.
        *   `search_params`: A dictionary allowing flexible query construction (e.g., `{"industries_names": "...", "countries": "...", ...}`).
        *   Uses `httpx.AsyncClient` for asynchronous HTTP requests.
        *   **Pagination Logic:** Implements pagination for the `/company/search` POST endpoint. It will use `page_number` and `page_size` (max 100, as specified) in the JSON request body. It will iterate, incrementing `page_number`, until `num_records_to_fetch` are retrieved or the API returns no more new results.
    *   Encapsulates API endpoint specifics, request formatting, and response parsing.
    *   Includes basic error handling and logging for API interactions.

### 3.4. LLM Service (`llm_service/`)

*   **`base_llm_client.py` (`BaseLLMClient`):**
    *   **Purpose:** Defines a common interface for all LLM clients.
    *   **Design:** An abstract base class (ABC) with an abstract method:
        `async def generate_structured_output(self, system_prompt: str, user_prompt_content: str, output_pydantic_model: Type[BaseModel]) -> BaseModel`.
        This ensures that any LLM client implementation will provide a consistent way to get structured JSON output validated by a Pydantic model.

*   **`gemini_client.py` (`GeminiLLMClient`):**
    *   **Purpose:** Gemini-specific LLM interaction.
    *   **Design:**
        *   Inherits from `BaseLLMClient`.
        *   Uses the `google-generativeai` library.
        *   Constructor takes API key and model name from `config.py`.
        *   Implements `generate_structured_output` by:
            *   Configuring the Gemini model for JSON output mode.
            *   Passing the system prompt and user prompt.
            *   Parsing the JSON response and validating it against the provided `output_pydantic_model`.

*   **`deepseek_client.py` (`DeepSeekLLMClient`):**
    *   **Purpose:** DeepSeek-specific LLM interaction.
    *   **Design:**
        *   Inherits from `BaseLLMClient`.
        *   Uses the `openai` Python library, configured with DeepSeek's API key and base URL.
        *   Implements `generate_structured_output` by:
            *   Setting `response_format={"type": "json_object"}` in the API call.
            *   Passing system and user prompts.
            *   Parsing the JSON response and validating it against the `output_pydantic_model`.

*   **`llm_factory.py` (`LLMFactory`):**
    *   **Purpose:** Decouples `main.py` and agents from specific LLM client instantiation.
    *   **Design:**
        *   A function `get_llm_client() -> BaseLLMClient`.
        *   Reads `config.LLM_VENDOR` and relevant API keys/model names from `config.py`.
        *   Returns an instance of `GeminiLLMClient` or `DeepSeekLLMClient` accordingly.
    *   **Design Decision:** This makes switching LLM providers a configuration change rather than a code change in multiple places.

### 3.5. Agents (`agents/`)

*   **`company_tags_agent.py` (`CompanyTagsAgent`):**
    *   **Purpose:** Responsible for the logic of enriching company data using an LLM.
    *   **Pydantic Model:** Defines `CompanyEnrichmentOutput(BaseModel)` with `industry_tags: List[str]` and `business_types: List[str]` for structured LLM output.
    *   **Design:**
        *   Constructor: `__init__(self, llm_client: BaseLLMClient)`.
        *   Core Method: `async generate_tags(self, company_context_for_llm: dict) -> CompanyEnrichmentOutput`.
            *   `company_context_for_llm` is the filtered, non-empty data for a single company.
            *   Constructs the system prompt (see updated version in previous turn) and a user prompt (e.g., "Analyze the following company data: {JSON_STRING_OF_company_context_for_llm}").
            *   Calls `self.llm_client.generate_structured_output()` with the prompts and `CompanyEnrichmentOutput` as the schema.
            *   If the LLM returns empty lists (e.g., `{"industry_tags": [], "business_types": []}`), this is considered a valid response indicating no tags could be confidently determined.

### 3.6. Utilities (`utils/`)

*   **`file_operations.py`:**
    *   **Purpose:** Generic helper functions for file I/O.
    *   **Functions:** `save_to_json(data: Any, filepath: str)` and `load_from_json(filepath: str) -> Any`.

*   **`data_extractor.py`:**
    *   **Purpose:** Extracts and filters relevant fields from the raw Neuron360 company profile to create a concise input for the LLM.
    *   **Function:** `extract_company_data_for_llm(full_company_profile: dict) -> dict`.
        *   **Logic:**
            1.  Maintains a predefined list/set of keys that are relevant for LLM processing (derived from `company_tags_agent_required_info.json`).
            2.  Iterates through these predefined keys. For each key:
                *   Checks if it exists in the `full_company_profile`.
                *   Retrieves the value.
                *   Validates that the value is not "empty" (e.g., `None`, empty string `""`, empty list `[]`, empty dictionary `{}`).
                *   If the key exists and its value is not empty, it's included in the returned dictionary.
        *   **Design Decision:** This ensures the LLM receives only pertinent, non-null information, optimizing token usage and potentially improving the quality of its analysis.

## 4. Data Storage

*   **Raw Neuron360 Data:**
    *   Location: `data/companies/neuron360_company_profiles.json`
    *   Format: A JSON list, where each item is a company profile dictionary as returned by Neuron360.
*   **Enriched Company Data:**
    *   Location: `data/companies/company_tags.json`
    *   Format: A JSON list, where each item is an object containing:
        *   `company_id`: A unique identifier from the Neuron360 profile.
        *   `neuron360_profile`: The original company profile data from Neuron360.
        *   `llm_enrichment`: The JSON object (`{"industry_tags": [...], "business_types": [...]}`) returned by the LLM.
        *   `llm_vendor_used`: A string indicating which LLM was used (e.g., "gemini", "deepseek").
        *   `enrichment_status`: A string indicating the outcome (e.g., "success", "empty_tags_returned", "error_processing").
*   **Design Decision:** Using local JSON files is suitable for this initial version for simplicity. Future iterations might involve migrating to a database like Supabase.

## 5. Important Logic & Design Decisions

*   **Standalone Project:** The `goldilocks-data` project is self-contained and does not directly depend on code from `goldilocks-backend`. Code reuse is achieved by adapting relevant concepts or snippets.
*   **Asynchronous Operations:** The use of `asyncio` for Neuron360 API calls and, more importantly, for concurrent LLM enrichment calls is crucial for performance. A semaphore (`asyncio.Semaphore`) in `main.py` controls the maximum number of concurrent LLM requests to manage resources and respect potential rate limits.
*   **LLM Abstraction & Factory:** The `BaseLLMClient` interface and `LLMFactory` allow for easy switching between Gemini and DeepSeek by changing a configuration value, promoting flexibility and easier future expansion to other LLM vendors.
*   **Structured LLM Output:** Pydantic models are used to define the expected JSON schema for LLM outputs. This allows for robust validation of the LLM's response. Both Gemini and DeepSeek clients will be configured to adhere to JSON mode.
*   **Configuration-Driven Parameters:** Key operational parameters (API keys, model names, concurrency limits) are managed through `config.py` and externalized to `.env` files, making the application adaptable without code changes.
*   **Specific Data Extraction for LLM:** The `utils.data_extractor.py` ensures that only relevant and non-empty fields are passed to the LLM, optimizing the prompt and potentially improving LLM performance and accuracy.
*   **Error Handling:** Basic error logging will be implemented for API calls and LLM interactions. For LLM enrichment, if an error occurs for a specific company, it will be logged, and the process will continue with other companies. The final output will indicate the status for each company.
*   **Neuron360 Pagination:** The `Neuron360APIClient` will handle pagination by using `page_number` and `page_size` in the request body, fetching records iteratively until the desired count (100) is reached or no more data is available. `page_size` will be set to 100.

## 6. Crucial Considerations & Future Work

*   **Rate Limiting (Advanced):** While `MAX_CONCURRENT_LLM_REQUESTS` and `LLM_REQUEST_DELAY_SECONDS` provide basic control, more sophisticated rate limiting might be needed if strict external API limits are encountered frequently. The Gemini RPM is high (2000/min), so this might be less of an issue initially for 100 records.
*   **Retry Mechanisms:** For this version, only basic error logging is planned. Future enhancements could include retry logic (e.g., with exponential backoff) for transient network errors or specific API error codes.
*   **Scalability:** For a much larger number of companies, the current approach of in-memory processing and local JSON files might become a bottleneck. Migrating to a proper database and potentially a task queue system would be necessary.
*   **LLM Prompt Iteration:** The provided system prompt is a starting point. It will likely require further iteration and refinement based on the actual quality of tags generated by the LLMs.
*   **Cost Management:** LLM calls incur costs. Processing a large number of records will have a direct cost implication that needs to be monitored.
*   **Detailed Logging & Monitoring:** For production use, more comprehensive logging and monitoring would be essential.

This design aims to provide a solid foundation for the initial version of the `goldilocks-data` project while keeping future scalability and enhancements in mind. 