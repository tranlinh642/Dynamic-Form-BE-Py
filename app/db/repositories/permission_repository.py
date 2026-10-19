from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.role import Permission
from app.db.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, session: AsyncSession):
        super().__init__(Permission, session)

    async def get_by_name(self, name: str) -> Optional[Permission]:
        stmt = select(Permission).where(Permission.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
