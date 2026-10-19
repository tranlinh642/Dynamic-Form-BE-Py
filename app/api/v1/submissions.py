from typing import Optional
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user, require_permissions
from app.core.constants import Permissions
from app.db.session import get_db
from app.schemas.form import FormResponse
from app.schemas.response import PaginatedResponse, SuccessResponse
from app.schemas.submission import SubmissionResponse, SubmitFormRequest
from app.services.submission_service import SubmissionService

router = APIRouter(tags=["Submissions"])


@router.get(
    "/forms/active",
    response_model=PaginatedResponse[FormResponse],
    summary="Lấy danh sách các form đang mở (active)",
)
async def get_active_forms(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    _: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubmissionService(db)
    forms, total = await service.get_active_forms(page=page, limit=limit)
    items = [FormResponse.model_validate(f) for f in forms]
    return PaginatedResponse.create(
        data=items,
        total=total,
        page=page,
        limit=limit,
        message="Lấy danh sách form đang mở thành công",
    )


@router.post(
    "/forms/{id}/submit",
    response_model=SuccessResponse[SubmissionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Nộp (Submit) form",
)
async def submit_form(
    id: uuid.UUID,
    req: SubmitFormRequest,
    current_user: dict = Depends(require_permissions(Permissions.SUBMIT_FORM)),
    db: AsyncSession = Depends(get_db),
):
    service = SubmissionService(db)
    submission = await service.submit_form(
        user_id=current_user["sub"],
        form_id=id,
        answers=req.answers,
    )
    return SuccessResponse.create(
        data=SubmissionResponse.model_validate(submission),
        message="Nộp form thành công",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/submissions",
    response_model=PaginatedResponse[SubmissionResponse],
    summary="Xem lịch sử nộp bài",
)
async def get_submissions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    all_subs: Optional[bool] = Query(default=False, alias="all"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubmissionService(db)
    user_perms = current_user.get("permissions", [])
    is_admin = Permissions.VIEW_ALL_SUBMISSIONS in user_perms

    if is_admin and all_subs:
        submissions, total = await service.get_all_submissions(
            page=page, limit=limit
        )
        items = [SubmissionResponse.model_validate(s) for s in submissions]
        return PaginatedResponse.create(
            data=items,
            total=total,
            page=page,
            limit=limit,
            message="Lấy tất cả lịch sử nộp bài thành công",
        )

    submissions, total = await service.get_user_submissions(
        user_id=current_user["sub"], page=page, limit=limit
    )
    items = [SubmissionResponse.model_validate(s) for s in submissions]
    return PaginatedResponse.create(
        data=items,
        total=total,
        page=page,
        limit=limit,
        message="Lấy lịch sử nộp bài thành công",
    )
