from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.role import Role, RolePermission
from app.db.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)

    async def get_by_name(self, name: str) -> Optional[Role]:
        stmt = (
            select(Role)
            .options(
                selectinload(Role.role_permissions).selectinload(
                    RolePermission.permission
                )
            )
            .where(Role.name == name)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
