from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class CustomBaseModel(BaseModel):
    """
    A custom base model that other Pydantic models can inherit from.
    It includes common fields and configurations.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None,
            UUID: lambda v: str(v) if v else None,
        },
        from_attributes=True,
    )

    id: Optional[int] = None
    uuid: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
