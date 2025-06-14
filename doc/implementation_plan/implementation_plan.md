---
title: Implementation Plan - Record Update Strategy
created_at: 2025-06-14
updated_at: 2025-06-14
status: Withhold
---

# Implementation Plan: Record Update Strategy

## 1. Context

The current data integration pipeline is designed to only **create** new records in the Supabase database. It does not account for scenarios where data for a given person or organisation already exists. This limitation prevents the system from processing updates, leading to data staleness and potential errors if the same data is processed multiple times.

The goal of this implementation is to introduce an **update-by-replacement** strategy. When processing a record (person or organisation) that already exists in the database (identified by its `neuron360` ID), the system will first **delete all** of its existing, related records before inserting the new version of the data. This ensures data consistency and that the database is an up-to-date reflection of the source.

### Legend for Task Status
- `[ ]` - To Do
- `[~]` - In Progress
- `[x]` - Done
- `[-]` - Blocked / Won't Do

## 2. Key Identifier Mappings

The update logic will rely on the following external-to-internal ID mappings:

-   **People**: `people.identities` maps the external `neuron360_profile_id` to the internal `people_id` (UUID).
-   **Organisations**: `organisation.identities` maps the external `neuron360_company_id` to the internal `organisation_id` (UUID).
-   **Offices**: `organisation.offices` maps the external `neuron360_office_id` to the internal `office_id` (UUID).

## 3. Implementation Phases

The implementation is broken down into four phases: enhancing the service layer, adding update logic to the organisation manager, adding update logic to the people manager, and finally, testing.

### Phase 1: Service Layer Enhancements

This phase focuses on adding the necessary deletion methods to the service layer. Since the database schema does not enforce cascading deletes (`ON DELETE CASCADE`), the application must be responsible for orchestrating the deletion of records in the correct order to avoid foreign key constraint violations.

**Tasks:**

-   `[ ]` **Analyse Foreign Key Dependencies**: Review the `people_and_org_data_schema.txt` to map out the exact deletion order required for each schema.
-   `[ ]` **Create Deletion Methods in `people_services.py`**:
    -   `[ ]` Implement `delete_by_people_id` in services for tables that have a direct foreign key to `people.identities` (e.g., `ProfileService`, `ExperienceService`, `EducationService`).
    -   `[ ]` Implement `delete_by_experience_id` for child tables of `experiences` (e.g., `JobTitleDetailService`, `JobFunctionService`).
    -   `[ ]` Implement similar deletion methods for children of `educations`, `certifications`, etc.
-   `[ ]` **Create Deletion Methods in `organisation_services.py`**:
    -   `[ ]` Implement `delete_by_organisation_id` for tables with a foreign key to `organisation.identities` (e.g., `WebAddressService`, `EmployeeService`, `OfficeService`).
    -   `[ ]` Implement `delete_by_office_id` for child tables of `offices` (e.g., `OfficeAddressService`, `OfficeIndustryService`).
-   `[ ]` **Update `BaseService`**:
    -   `[ ]` Add a generic `delete_by_column` method to `BaseService` to reduce code duplication in the specific service files. The method signature should be `delete_by_column(self, column_name: str, value: Any) -> bool`.

### Phase 2: Manager Layer - Organisation Update Logic

With the service layer updated, this phase implements the core update logic in the `OrganisationManager`.

**Tasks:**

-   `[ ]` **Modify `OrganisationManager.process_organisation_data`**:
    -   `[ ]` Use the existing `identity_service.get_by_neuron_id()` to check if an organisation with the given `neuron360_company_id` exists.
    -   `[ ]` If it exists:
        -   `[ ]` Log that an existing organisation is being updated.
        -   `[ ]` Get the `organisation_id` from the existing identity.
        -   `[ ]` Create a new private method `_delete_organisation_data(self, organisation_id: uuid.UUID)`.
        -   `[ ]` Within `_delete_organisation_data`, call all the necessary `delete_by_organisation_id` and `delete_by_office_id` service methods in the correct dependency order. This includes deleting all offices associated with the organisation.
        -   `[ ]` Finally, delete the `organisation.identities` record itself.
    -   `[ ]` Proceed with the existing logic to create the new organisation records from scratch.
-   `[ ]` **Refactor `OrganisationManager._process_office`**: The logic for deleting an organisation should also handle its offices. However, if office data can be updated independently, a similar check-and-delete logic using `neuron360_office_id` might be needed here. For now, we assume deleting the parent organisation is sufficient.

### Phase 3: Manager Layer - People Update Logic

This phase mirrors Phase 2, applying the update logic to the `PeopleManager`.

**Tasks:**

-   `[ ]` **Modify `PeopleManager.process_person_data`**:
    -   `[ ]` At the beginning of the method, use `identity_service.get_by_neuron_id()` to check for an existing person via `neuron360_profile_id`.
    -   `[ ]` If an identity is found:
        -   `[ ]` Log that an existing person's record is being updated.
        -   `[ ]` Get the `people_id`.
        -   `[ ]` Create a new private method `_delete_person_data(self, people_id: uuid.UUID)`.
        -   `[ ]` This method will be responsible for calling all the `delete_by...` methods in the `people_services` in the correct order to remove all of a person's data (profile, experiences, education, etc.).
        -   `[ ]` Finally, delete the `people.identities` record.
    -   `[ ]` Proceed with the existing record creation logic. **Note**: The call to `org_manager.process_organisation_data` should remain, as it has its own idempotency check from Phase 2.

### Phase 4: Testing and Validation

This final phase ensures the new logic is working correctly and hasn't introduced regressions.

**Tasks:**

-   `[ ]` **Unit Tests**:
    -   `[ ]` Write unit tests for the new `delete_by_...` methods in the service layers.
-   `[ ]` **Integration Tests**:
    -   `[ ]` Create a new test file `tests/integration/test_update_logic.py`.
    -   `[ ]` **Test Case 1**: Process a JSON file, then process it again. Assert that the final state of the database is correct and that no duplicate records exist.
    -   `[ ]` **Test Case 2**: Process a file. Manually alter a value in a table (e.g., a person's name). Process the original file again. Assert that the altered value has been reverted to its original state.
    -   `[ ]` **Test Case 3**: Verify that processing a person with an existing organisation does not delete and re-create the organisation if the organisation data is unchanged (leveraging the check in `OrganisationManager`).
