# Goldilocks-Data: Implementation Plan

## 1. Project Goal

The primary goal of this initial implementation is to build a Python application that:
1.  Fetches 100 company profiles from the Neuron360 API based on specified search criteria.
2.  Stores these raw profiles locally.
3.  For each company, extracts relevant information and uses an LLM (configurable between Gemini and DeepSeek) to enrich the profile with `industry_tags` and `business_types`.
4.  The LLM enrichment process should be asynchronous to handle multiple companies concurrently.
5.  Stores the enriched company data, including the original profile and the LLM-generated tags, locally.

## 2. Components to be Implemented

Based on the System Design Document, the following key components will be created:

*   **Project Setup:** Virtual environment, `requirements.txt`, `.env` files, basic directory structure.
*   **Configuration (`config.py`):** Manages API keys, model names, URLs, and concurrency settings.
*   **Utilities:**
    *   `utils/file_operations.py`: For saving and loading JSON data.
    *   `utils/data_extractor.py`: For preparing company data for LLM input.
*   **Neuron360 Service:**
    *   `neuron360_service/client.py` (`Neuron360APIClient`): Handles API communication and pagination.
*   **LLM Service:**
    *   `llm_service/base_llm_client.py` (`BaseLLMClient`): Abstract base class for LLM clients.
    *   `llm_service/gemini_client.py` (`GeminiLLMClient`): Gemini-specific implementation.
    *   `llm_service/deepseek_client.py` (`DeepSeekLLMClient`): DeepSeek-specific implementation.
    *   `llm_service/llm_factory.py` (`LLMFactory`): To get a configured LLM client instance.
*   **Agent:**
    *   `agents/company_tags_agent.py` (`CompanyTagsAgent`): Orchestrates LLM prompting and processes results for company tagging. Includes the Pydantic model for LLM output schema.
*   **Main Orchestrator (`main.py`):** Drives the entire workflow, from data fetching to enrichment and final storage, handling asynchronous operations.
*   **Data Storage:** Local JSON files in `data/companies/` for raw and enriched data.

## 3. Task List & Status

**Legend for Status Indicators:**
*   `[ ]` - To Do
*   `[/]` - In Progress
*   `[x]` - Done
*   `[!]` - Blocked/Issue

### Phase 0: Project Setup & Initialization
*   `[ ]` **P0.1:** Create core project directory structure within `goldilocks-data` (data, neuron360_service, llm_service, agents, utils, docs, docs/design_docs).
*   `[ ]` **P0.2:** Initialize Python virtual environment (`venv`).
*   `[ ]` **P0.3:** Create and populate `requirements.txt` (google-generativeai, httpx, pydantic, python-dotenv, openai).
*   `[ ]` **P0.4:** Install dependencies from `requirements.txt`.
*   `[ ]` **P0.5:** Create `.env.example` with placeholders for API keys and configurations.
*   `[ ]` **P0.6:** Create `.env` file (from `.env.example`) and add actual API keys (ensure `.env` is in `.gitignore`).
*   `[ ]` **P0.7:** Create `__init__.py` files in all package directories (neuron360_service, llm_service, agents, utils).
*   `[ ]` **P0.8:** Initialize Git repository (`git init`) and make an initial commit of the project structure.
*   `[ ]` **P0.9:** Implement `config.py` to load settings from `.env` (API keys, model names, LLM_VENDOR, MAX_CONCURRENT_LLM_REQUESTS, etc.).
*   `[ ]` **P0.10:** Implement `utils/file_operations.py` with `save_to_json` and `load_from_json` functions.

### Phase 1: Neuron360 Data Fetching
*   `[ ]` **P1.1:** Implement `neuron360_service/client.py` (`Neuron360APIClient`).
    *   `[ ]` Constructor (`api_key`, `base_url`).
    *   `[ ]` `async search_companies(search_params, num_records_to_fetch)` method using `httpx.AsyncClient`.
    *   `[ ]` Implement pagination logic for `/company/search` (POST, `page_number`, `page_size`=100).
    *   `[ ]` Basic error logging for API calls.
*   `[ ]` **P1.2:** Update `main.py` (initial version) to test Neuron360 fetching.
    *   `[ ]` Load config, instantiate `Neuron360APIClient`.
    *   `[ ]` Define search parameters and call `search_companies` for 100 records.
    *   `[ ]` Save results to `data/companies/neuron360_company_profiles.json`.
    *   `[ ]` Add `asyncio.run()` for testing this part.

### Phase 2: LLM Integration & Data Processing Logic
*   `[ ]` **P2.1:** Implement `utils/data_extractor.py` (`extract_company_data_for_llm` function) to filter company profiles based on `company_tags_agent_required_info.json` and exclude empty fields.
*   `[ ]` **P2.2:** Define `CompanyEnrichmentOutput` Pydantic model in `agents/company_tags_agent.py`.
*   `[ ]` **P2.3:** Implement `llm_service/base_llm_client.py` (`BaseLLMClient` abstract class with `async generate_structured_output`).
*   `[ ]` **P2.4:** Implement `llm_service/gemini_client.py` (`GeminiLLMClient`).
    *   `[ ]` Inherit `BaseLLMClient`.
    *   `[ ]` Implement `generate_structured_output` for Gemini (JSON mode).
*   `[ ]` **P2.5:** Implement `llm_service/deepseek_client.py` (`DeepSeekLLMClient`).
    *   `[ ]` Inherit `BaseLLMClient`.
    *   `[ ]` Implement `generate_structured_output` for DeepSeek (JSON mode using OpenAI library).
*   `[ ]` **P2.6:** Implement `llm_service/llm_factory.py` (`get_llm_client` function) to return configured LLM client.
*   `[ ]` **P2.7:** Implement `agents/company_tags_agent.py` (`CompanyTagsAgent`).
    *   `[ ]` Constructor taking `BaseLLMClient`.
    *   `[ ]` Store updated system prompt.
    *   `[ ]` Implement `async generate_tags(company_context_for_llm)` method.

### Phase 3: Main Orchestration - Asynchronous Enrichment
*   `[ ]` **P3.1:** Update `main.py` for the full asynchronous orchestration.
    *   `[ ]` Load `neuron360_company_profiles.json`.
    *   `[ ]` Initialize LLM client via factory and `CompanyTagsAgent`.
    *   `[ ]` Implement `asyncio.Semaphore` for concurrency control.
    *   `[ ]` Create `process_company` async helper function to: extract data, call agent, handle LLM response/errors, include delay if configured.
    *   `[ ]` Use `asyncio.gather` to run `process_company` for all profiles.
    *   `[ ]` Format and collect all enriched data (including original profile, tags, vendor, status).
    *   `[ ]` Save final results to `data/companies/company_tags.json`.
    *   `[ ]` Add basic `logging.basicConfig`.
*   `[ ]` **P3.2:** Thorough testing.
    *   `[ ]` Test with a small number of records.
    *   `[ ]` Test switching `LLM_VENDOR` in `config.py`.
    *   `[ ]` Verify output JSON structure and content.
    *   `[ ]` Monitor logs for errors.

## 4. Documentation (Ongoing)
*   `[x]` **DOC.1:** Create System Design Document (`docs/design_docs/SYSTEM_DESIGN.md`).
*   `[x]` **DOC.2:** Create this Implementation Plan Document (`docs/IMPLEMENTATION_PLAN.md`).
*   `[ ]` **DOC.3:** Add README.md to the root of `goldilocks-data` with setup and usage instructions.
*   `[ ]` **DOC.4:** Add docstrings and comments to code as developed.

This implementation plan provides a structured approach to developing the `goldilocks-data` application. Status will be updated as tasks are completed. 