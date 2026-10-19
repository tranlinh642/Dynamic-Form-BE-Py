from typing import List, Tuple
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.submission import Submission
from app.db.repositories.base import BaseRepository


class SubmissionRepository(BaseRepository[Submission]):
    def __init__(self, session: AsyncSession):
        super().__init__(Submission, session)

    async def get_user_submissions(
        self, user_id: uuid.UUID | str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Submission], int]:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)

        count_stmt = (
            select(func.count())
            .select_from(Submission)
            .where(Submission.user_id == user_id)
        )
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = (
            select(Submission)
            .options(selectinload(Submission.form))
            .where(Submission.user_id == user_id)
            .order_by(Submission.submitted_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_all_submissions(
        self, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Submission], int]:
        count_stmt = select(func.count()).select_from(Submission)
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = (
            select(Submission)
            .options(
                selectinload(Submission.form),
                selectinload(Submission.user),
            )
            .order_by(Submission.submitted_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total
