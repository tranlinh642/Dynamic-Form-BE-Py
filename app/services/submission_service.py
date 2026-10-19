from typing import Any, List, Tuple
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import FormStatus
from app.core.exceptions import NotFoundException, ValidationException
from app.core.validation.validation_factory import ValidationFactory
from app.db.models.form import Form
from app.db.models.submission import Submission
from app.db.repositories.form_repository import FormRepository
from app.db.repositories.submission_repository import SubmissionRepository
from app.schemas.submission import SubmitAnswerItem


class SubmissionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.form_repo = FormRepository(session)
        self.submission_repo = SubmissionRepository(session)

    async def get_active_forms(
        self, page: int = 1, limit: int = 10
    ) -> Tuple[List[Form], int]:
        skip = (page - 1) * limit
        return await self.form_repo.get_active_forms(skip=skip, limit=limit)

    async def submit_form(
        self,
        user_id: uuid.UUID | str,
        form_id: uuid.UUID | str,
        answers: List[SubmitAnswerItem],
    ) -> Submission:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        if isinstance(form_id, str):
            form_id = uuid.UUID(form_id)

        form = await self.form_repo.get_by_id_with_fields(form_id)
        if not form or form.status != FormStatus.ACTIVE.value:
            raise NotFoundException("Form không tồn tại hoặc chưa kích hoạt")

        answer_map: dict[str, Any] = {
            str(item.fieldId): item.value for item in answers
        }

        errors: List[str] = []
        raw_answers_payload = []

        for field in form.fields:
            field_key = str(field.id)
            val = answer_map.get(field_key)

            if field.is_required and (val is None or val == ""):
                errors.append(f"Trường {field.label} là bắt buộc.")
                continue

            if val is not None and val != "":
                validator = ValidationFactory.get_validator(field.type)
                err = validator.validate(val, field)
                if err:
                    errors.append(err)

            if val is not None:
                raw_answers_payload.append(
                    {"fieldId": field_key, "value": val}
                )

        if errors:
            raise ValidationException(
                message="Dữ liệu không hợp lệ", errors=errors
            )

        submission = Submission(
            form_id=form_id,
            user_id=user_id,
            answers=raw_answers_payload,
        )
        return await self.submission_repo.create(submission)

    async def get_user_submissions(
        self, user_id: uuid.UUID | str, page: int = 1, limit: int = 10
    ) -> Tuple[List[Submission], int]:
        skip = (page - 1) * limit
        return await self.submission_repo.get_user_submissions(
            user_id=user_id, skip=skip, limit=limit
        )

    async def get_all_submissions(
        self, page: int = 1, limit: int = 10
    ) -> Tuple[List[Submission], int]:
        skip = (page - 1) * limit
        return await self.submission_repo.get_all_submissions(
            skip=skip, limit=limit
        )
