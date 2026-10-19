from typing import List, Optional, Tuple
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import FormStatus
from app.core.exceptions import NotFoundException
from app.db.models.form import Form
from app.db.repositories.form_repository import FormRepository
from app.schemas.form import CreateFormRequest, UpdateFormRequest


class FormService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.form_repo = FormRepository(session)

    async def create_form(
        self, user_id: uuid.UUID | str, req: CreateFormRequest
    ) -> Form:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)

        new_form = Form(
            title=req.title,
            description=req.description,
            order=req.order,
            status=FormStatus.DRAFT.value,
            created_by=user_id,
        )
        return await self.form_repo.create(new_form)

    async def get_forms(
        self, page: int = 1, limit: int = 10, status: Optional[str] = None
    ) -> Tuple[List[Form], int]:
        skip = (page - 1) * limit
        return await self.form_repo.get_forms(
            skip=skip, limit=limit, status=status
        )

    async def get_form_by_id(self, form_id: uuid.UUID | str) -> Form:
        form = await self.form_repo.get_by_id_with_fields(form_id)
        if not form:
            raise NotFoundException("Không tìm thấy form")
        return form

    async def update_form(
        self, form_id: uuid.UUID | str, req: UpdateFormRequest
    ) -> Form:
        form = await self.get_form_by_id(form_id)

        if req.title is not None:
            form.title = req.title
        if req.description is not None:
            form.description = req.description
        if req.order is not None:
            form.order = req.order
        if req.status is not None:
            form.status = req.status.value

        await self.form_repo.update(form)
        return await self.get_form_by_id(form_id)

    async def delete_form(self, form_id: uuid.UUID | str) -> None:
        form = await self.get_form_by_id(form_id)
        await self.form_repo.delete(form)

    async def update_form_orders(self, orders: List[dict]) -> None:
        await self.form_repo.update_orders(orders)
