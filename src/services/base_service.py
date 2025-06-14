from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from src.utils.config import config
from src.utils.logging import logger
from typing import Type, TypeVar, List, Dict, Any
from pydantic import BaseModel
import uuid
import json

T = TypeVar("T", bound=BaseModel)


class BaseService:
    """
    A base service with common CRUD operations for Supabase tables.
    Each service instance will have its own Supabase client configured for the correct schema.
    """

    def __init__(self, table_name: str, model: Type[T]):
        self.table_name = table_name
        self.model = model

        # Determine schema from table name (e.g., 'people' from 'people.identities')
        schema = table_name.split(".")[0]
        options = ClientOptions(schema=schema)

        # Create a dedicated client for this service's schema
        self.client = create_client(
            config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY, options
        )

    def create(self, data: T) -> T:
        """
        Creates a new record in the table.
        """
        try:
            # Manually create a JSON-serializable dictionary
            record_json = data.model_dump_json(by_alias=True)
            record_dict = json.loads(record_json)

            # Filter out None values to avoid issues with non-nullable columns
            record_dict = {k: v for k, v in record_dict.items() if v is not None}
            table_name_only = self.table_name.split(".")[1]
            response = self.client.table(table_name_only).insert(record_dict).execute()

            if response.data:
                logger.info(f"Successfully created record in {self.table_name}")
                return self.model.model_validate(response.data[0])
            else:
                logger.error(
                    f"Failed to create record in {self.table_name}: No data returned"
                )
                return None
        except Exception as e:
            logger.error(f"Error creating record in {self.table_name}: {e}")
            return None

    def get_by_id(self, record_id: any) -> T:
        """
        Retrieves a record by its primary key.
        """
        try:
            table_name_only = self.table_name.split(".")[1]
            response = (
                self.client.table(table_name_only)
                .select("*")
                .eq("id", record_id)
                .execute()
            )
            if response.data:
                return self.model.model_validate(response.data[0])
            return None
        except Exception as e:
            logger.error(
                f"Error fetching record {record_id} from {self.table_name}: {e}"
            )
            return None

    def get_by_uuid(self, record_uuid: uuid.UUID) -> T:
        """
        Retrieves a record by its UUID.
        """
        try:
            table_name_only = self.table_name.split(".")[1]
            response = (
                self.client.table(table_name_only)
                .select("*")
                .eq("uuid", str(record_uuid))
                .execute()
            )
            if response.data:
                return self.model.model_validate(response.data[0])
            return None
        except Exception as e:
            logger.error(
                f"Error fetching record {record_uuid} from {self.table_name}: {e}"
            )
            return None

    def get_by_neuron_id(self, neuron_id: str) -> T:
        """
        Retrieves a record by its neuron360 ID.
        This is a common pattern for organisations and people.
        """
        try:
            table_name_only = self.table_name.split(".")[1]
            # Figure out the correct column name based on the table
            if table_name_only == "identities" and "organisation" in self.table_name:
                id_column = "neuron360_company_id"
            elif table_name_only == "identities" and "people" in self.table_name:
                id_column = "neuron360_profile_id"
            elif table_name_only == "offices":
                id_column = "neuron360_office_id"
            else:
                logger.error(
                    f"get_by_neuron_id is not supported for table {self.table_name}"
                )
                return None

            response = (
                self.client.table(table_name_only)
                .select("*")
                .eq(id_column, neuron_id)
                .limit(1)
                .execute()
            )
            if response.data:
                return self.model.model_validate(response.data[0])
                return None
        except Exception as e:
            logger.error(
                f"Error fetching record with neuron_id {neuron_id} from {self.table_name}: {e}"
            )
            return None

    def get_all(self, limit: int = 100) -> List[T]:
        """
        Retrieves all records from the table with a limit.
        """
        try:
            table_name_only = self.table_name.split(".")[1]
            response = (
                self.client.table(table_name_only).select("*").limit(limit).execute()
            )
            if response.data:
                return [self.model.model_validate(item) for item in response.data]
            return []
        except Exception as e:
            logger.error(f"Error fetching all records from {self.table_name}: {e}")
            return []

    def delete(self, record_id: Any) -> bool:
        """
        Deletes a record by its primary key.
        """
        try:
            table_name_only = self.table_name.split(".")[1]
            response = (
                self.client.table(table_name_only)
                .delete()
                .eq("id", record_id)
                .execute()
            )
            if response.data:
                logger.info(
                    f"Successfully deleted record {record_id} from {self.table_name}"
                )
                return True
            else:
                logger.warning(
                    f"Record {record_id} not found in {self.table_name} for deletion."
                )
                return False
        except Exception as e:
            logger.error(
                f"Error deleting record {record_id} from {self.table_name}: {e}"
            )
            return False

    def upsert(self, data: T, on_conflict: str = "id") -> T:
        """
        Performs an 'upsert' operation (insert or update).
        """
        try:
            # Manually create a JSON-serializable dictionary
            record_json = data.model_dump_json(by_alias=True)
            record_dict = json.loads(record_json)

            # Filter out None values to avoid issues with non-nullable columns
            record_dict = {k: v for k, v in record_dict.items() if v is not None}
            table_name_only = self.table_name.split(".")[1]
            response = (
                self.client.table(table_name_only)
                .upsert(record_dict, on_conflict=on_conflict)
                .execute()
            )

            if response.data:
                logger.info(f"Successfully upserted record in {self.table_name}")
                return self.model.model_validate(response.data[0])
            else:
                logger.error(f"Failed to upsert record in {self.table_name}")
                return None
        except Exception as e:
            logger.error(f"Error upserting record in {self.table_name}: {e}")
            return None
