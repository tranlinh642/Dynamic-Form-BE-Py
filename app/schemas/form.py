from typing import List, Optional
import uuid
from pydantic import BaseModel, Field

from app.core.enums import FormStatus
from app.schemas.field import FieldResponse


class CreateFormRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    order: int = 0


class UpdateFormRequest(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    order: Optional[int] = None
    status: Optional[FormStatus] = None


class FormOrderItem(BaseModel):
    id: uuid.UUID
    order: int


class UpdateFormOrdersRequest(BaseModel):
    orders: List[FormOrderItem]


class FormResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    order: int
    status: str
    createdBy: uuid.UUID = Field(validation_alias="created_by")
    fields: Optional[List[FieldResponse]] = []

    class Config:
        from_attributes = True
        populate_by_name = True
