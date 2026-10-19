from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.role import Permission, Role, RolePermission
from app.db.models.user import User, UserRole
from app.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = (
            select(User)
            .options(
                selectinload(User.user_roles).selectinload(UserRole.role)
            )
            .where(User.email == email)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = (
            select(User)
            .options(
                selectinload(User.user_roles).selectinload(UserRole.role)
            )
            .where(User.username == username)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_with_roles(self, user_id: uuid.UUID | str) -> Optional[User]:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        stmt = (
            select(User)
            .options(
                selectinload(User.user_roles).selectinload(UserRole.role)
            )
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_permissions_by_user_id(
        self, user_id: uuid.UUID | str
    ) -> List[str]:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)

        stmt = (
            select(Permission.name)
            .distinct()
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
