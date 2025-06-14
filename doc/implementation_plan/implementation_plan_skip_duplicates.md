---
title: Implementation Plan - Duplicate Record Handling
created_at: 2025-06-14
updated_at: 2025-06-14
---

# Implementation Plan: Duplicate Record Handling

## 1. Context

The data processing pipeline currently creates new records for every person processed from the source file. This can lead to duplicate entries if the same person's data is ingested multiple times.

The goal is to introduce a check at the beginning of the person processing workflow. The system will query the `people.identities` table to see if a record with the given `neuron360_profile_id` already exists. If it does, the pipeline will skip processing for that entire person record, preventing redundant data entry.

The `OrganisationManager` already implements a similar and correct logic for organisations and offices, so no changes are required there.

## 2. Implementation Steps

### Phase 1: Update PeopleManager Logic 🟢

-   **Task 1: Add Duplicate Check in `process_person_data`** 🟢
    -   **File**: `src/managers/people_manager.py`
    -   **Method**: `process_person_data`
    -   **Logic**:
        1.  At the beginning of the `try` block, extract the `neuron360_profile_id` from the `profile_data`.
        2.  If the `neuron360_profile_id` is present, call the `self.identity_service.get_by_neuron_id()` method to check if a record with this ID already exists in the database.
        3.  If an `existing_identity` is found, log an informational message indicating that the person is being skipped and `return` from the method immediately.
        4.  If no existing identity is found, the processing should continue as normal.

-   **Example Code Snippet (for planning purposes):**

    ```python
    # In src/managers/people_manager.py, inside process_person_data()

    try:
        profile_data = person_record.get("profile_data", {})
        resume_data = person_record.get("resume_data", {})

        if not profile_data:
            self._log_error("No 'profile_data' found, skipping record.")
            return

        # === START: New Duplicate Check Logic ===
        neuron_id = profile_data.get("profile_id")
        if neuron_id:
            existing_identity = self.identity_service.get_by_neuron_id(neuron_id)
            if existing_identity:
                self.logger.info(
                    f"Skipping existing Person with neuron_id: {neuron_id}"
                )
                return
        # === END: New Duplicate Check Logic ===

        self.logger.info(
            f"Processing person: {profile_data.get('profile_full_name')}"
        )

        # 1. Create Identity
        # ... (rest of the method remains the same)
    ```

### Phase 2: Testing and Validation 🟢

-   **Task 1: Manual Test** 🟢
    -   Run the `main.py` script twice using the same example data file.
    -   Observe the logs to confirm that on the second run, all person records are identified as duplicates and skipped, and no "create" operations are logged for people.
