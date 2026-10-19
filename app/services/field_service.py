from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.db.models.field import Field
from app.db.repositories.field_repository import FieldRepository
from app.db.repositories.form_repository import FormRepository
from app.schemas.field import AddFieldRequest, UpdateFieldRequest


class FieldService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.form_repo = FormRepository(session)
        self.field_repo = FieldRepository(session)

    async def add_field(
        self, form_id: uuid.UUID | str, req: AddFieldRequest
    ) -> Field:
        if isinstance(form_id, str):
            form_id = uuid.UUID(form_id)

        form = await self.form_repo.get_by_id(form_id)
        if not form:
            raise NotFoundException("Form không tồn tại")

        new_field = Field(
            form_id=form_id,
            label=req.label,
            type=req.type.value,
            order=req.order,
            is_required=req.isRequired,
            options=req.options,
            validation=req.validation,
        )
        return await self.field_repo.create(new_field)

    async def update_field(
        self,
        form_id: uuid.UUID | str,
        field_id: uuid.UUID | str,
        req: UpdateFieldRequest,
    ) -> Field:
        field = await self.field_repo.get_by_id_and_form_id(field_id, form_id)
        if not field:
            raise NotFoundException("Field hoặc Form không tồn tại")

        if req.label is not None:
            field.label = req.label
        if req.type is not None:
            field.type = req.type.value
        if req.order is not None:
            field.order = req.order
        if req.isRequired is not None:
            field.is_required = req.isRequired
        if req.options is not None:
            field.options = req.options
        if req.validation is not None:
            field.validation = req.validation

        return await self.field_repo.update(field)

    async def delete_field(
        self, form_id: uuid.UUID | str, field_id: uuid.UUID | str
    ) -> None:
        field = await self.field_repo.get_by_id_and_form_id(field_id, form_id)
        if not field:
            raise NotFoundException("Field hoặc Form không tồn tại")
        await self.field_repo.delete(field)

    async def update_field_orders(
        self, form_id: uuid.UUID | str, orders: List[dict]
    ) -> None:
        form = await self.form_repo.get_by_id(form_id)
        if not form:
            raise NotFoundException("Form không tồn tại")
        await self.field_repo.update_orders(form_id, orders)
