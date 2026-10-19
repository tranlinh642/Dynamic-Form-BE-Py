from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.field import Field
from app.db.repositories.base import BaseRepository


class FieldRepository(BaseRepository[Field]):
    def __init__(self, session: AsyncSession):
        super().__init__(Field, session)

    async def get_by_form_id(self, form_id: uuid.UUID | str) -> List[Field]:
        if isinstance(form_id, str):
            form_id = uuid.UUID(form_id)

        stmt = (
            select(Field)
            .where(Field.form_id == form_id)
            .order_by(Field.order.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id_and_form_id(
        self, field_id: uuid.UUID | str, form_id: uuid.UUID | str
    ) -> Optional[Field]:
        if isinstance(field_id, str):
            field_id = uuid.UUID(field_id)
        if isinstance(form_id, str):
            form_id = uuid.UUID(form_id)

        stmt = select(Field).where(
            Field.id == field_id, Field.form_id == form_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_orders(
        self, form_id: uuid.UUID | str, orders: List[dict]
    ) -> None:
        if isinstance(form_id, str):
            form_id = uuid.UUID(form_id)

        for item in orders:
            field_id = item["id"]
            if isinstance(field_id, str):
                field_id = uuid.UUID(field_id)
            field = await self.get_by_id_and_form_id(field_id, form_id)
            if field:
                field.order = item["order"]
        await self.session.flush()
