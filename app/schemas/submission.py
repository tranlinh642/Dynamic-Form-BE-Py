from datetime import datetime
from typing import Any, List, Optional
import uuid
from pydantic import BaseModel, Field


class SubmitAnswerItem(BaseModel):
    fieldId: uuid.UUID
    value: Any


class SubmitFormRequest(BaseModel):
    answers: List[SubmitAnswerItem]


class SubmissionFormInfo(BaseModel):
    id: uuid.UUID
    title: str

    class Config:
        from_attributes = True


class SubmissionUserInfo(BaseModel):
    id: uuid.UUID
    username: str
    email: str

    class Config:
        from_attributes = True


class SubmissionResponse(BaseModel):
    id: uuid.UUID
    formId: uuid.UUID = Field(validation_alias="form_id")
    userId: uuid.UUID = Field(validation_alias="user_id")
    submittedAt: datetime = Field(validation_alias="submitted_at")
    answers: Any
    form: Optional[SubmissionFormInfo] = None
    user: Optional[SubmissionUserInfo] = None

    class Config:
        from_attributes = True
        populate_by_name = True
