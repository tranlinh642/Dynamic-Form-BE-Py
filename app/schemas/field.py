from typing import Any, List, Optional
import uuid
from pydantic import BaseModel, Field

from app.core.enums import FieldType


class AddFieldRequest(BaseModel):
    label: str = Field(min_length=1, max_length=255)
    type: FieldType
    order: int = 0
    isRequired: bool = Field(default=False, alias="isRequired")
    options: Optional[List[Any]] = None
    validation: Optional[dict] = None

    class Config:
        populate_by_name = True


class UpdateFieldRequest(BaseModel):
    label: Optional[str] = Field(default=None, max_length=255)
    type: Optional[FieldType] = None
    order: Optional[int] = None
    isRequired: Optional[bool] = Field(default=None, alias="isRequired")
    options: Optional[List[Any]] = None
    validation: Optional[dict] = None

    class Config:
        populate_by_name = True


class FieldOrderItem(BaseModel):
    id: uuid.UUID
    order: int


class UpdateFieldOrdersRequest(BaseModel):
    orders: List[FieldOrderItem]


class FieldResponse(BaseModel):
    id: uuid.UUID
    formId: uuid.UUID = Field(validation_alias="form_id")
    label: str
    type: str
    order: int
    isRequired: bool = Field(validation_alias="is_required")
    options: Optional[Any] = None
    validation: Optional[Any] = None

    class Config:
        from_attributes = True
        populate_by_name = True
