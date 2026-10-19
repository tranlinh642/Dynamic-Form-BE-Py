from typing import List, Optional, Tuple
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.field import Field
from app.db.models.form import Form
from app.db.repositories.base import BaseRepository


class FormRepository(BaseRepository[Form]):
    def __init__(self, session: AsyncSession):
        super().__init__(Form, session)

    async def get_by_id_with_fields(
        self, form_id: uuid.UUID | str
    ) -> Optional[Form]:
        if isinstance(form_id, str):
            form_id = uuid.UUID(form_id)

        stmt = (
            select(Form)
            .options(
                selectinload(
                    Form.fields.and_(True)
                )
            )
            .where(Form.id == form_id)
        )
        result = await self.session.execute(stmt)
        form = result.scalar_one_or_none()
        if form and form.fields:
            form.fields.sort(key=lambda f: f.order)
        return form

    async def get_forms(
        self, skip: int = 0, limit: int = 10, status: Optional[str] = None
    ) -> Tuple[List[Form], int]:
        base_query = select(Form)
        count_query = select(func.count()).select_from(Form)

        if status:
            base_query = base_query.where(Form.status == status)
            count_query = count_query.where(Form.status == status)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        stmt = (
            base_query.options(selectinload(Form.fields))
            .order_by(Form.order.asc(), Form.id.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        forms = list(result.scalars().all())
        for f in forms:
            if f.fields:
                f.fields.sort(key=lambda item: item.order)

        return forms, total

    async def get_active_forms(
        self, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Form], int]:
        return await self.get_forms(skip=skip, limit=limit, status="active")

    async def update_orders(self, orders: List[dict]) -> None:
        for item in orders:
            form_id = item["id"]
            if isinstance(form_id, str):
                form_id = uuid.UUID(form_id)
            form = await self.get_by_id(form_id)
            if form:
                form.order = item["order"]
        await self.session.flush()
