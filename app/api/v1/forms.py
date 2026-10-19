from typing import Optional
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user, require_permissions
from app.core.constants import Permissions
from app.core.enums import FormStatus
from app.db.session import get_db
from app.schemas.form import (
    CreateFormRequest,
    FormResponse,
    UpdateFormOrdersRequest,
    UpdateFormRequest,
)
from app.schemas.response import PaginatedResponse, SuccessResponse
from app.services.form_service import FormService

router = APIRouter(prefix="/forms", tags=["Forms"])


@router.post(
    "",
    response_model=SuccessResponse[FormResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Tạo form mới",
)
async def create_form(
    req: CreateFormRequest,
    current_user: dict = Depends(require_permissions(Permissions.CREATE_FORM)),
    db: AsyncSession = Depends(get_db),
):
    service = FormService(db)
    form = await service.create_form(current_user["sub"], req)
    return SuccessResponse.create(
        data=FormResponse.model_validate(form),
        message="Tạo form thành công",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "",
    response_model=PaginatedResponse[FormResponse],
    summary="Lấy danh sách forms",
)
async def get_forms(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    form_status: Optional[FormStatus] = Query(default=None, alias="status"),
    _: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = FormService(db)
    status_val = form_status.value if form_status else None
    forms, total = await service.get_forms(
        page=page, limit=limit, status=status_val
    )
    items = [FormResponse.model_validate(f) for f in forms]
    return PaginatedResponse.create(
        data=items,
        total=total,
        page=page,
        limit=limit,
        message="Lấy danh sách form thành công",
    )


@router.put(
    "/order",
    response_model=SuccessResponse[None],
    summary="Cập nhật thứ tự sắp xếp của nhiều form",
)
async def update_form_orders(
    req: UpdateFormOrdersRequest,
    _: dict = Depends(require_permissions(Permissions.UPDATE_FORM)),
    db: AsyncSession = Depends(get_db),
):
    service = FormService(db)
    orders_data = [item.model_dump() for item in req.orders]
    await service.update_form_orders(orders_data)
    return SuccessResponse.create(
        data=None, message="Cập nhật thứ tự form thành công"
    )


@router.get(
    "/{id}",
    response_model=SuccessResponse[FormResponse],
    summary="Lấy chi tiết form theo ID",
)
async def get_form_by_id(
    id: uuid.UUID,
    _: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = FormService(db)
    form = await service.get_form_by_id(id)
    return SuccessResponse.create(
        data=FormResponse.model_validate(form),
        message="Lấy chi tiết form thành công",
    )


@router.put(
    "/{id}",
    response_model=SuccessResponse[FormResponse],
    summary="Cập nhật form",
)
async def update_form(
    id: uuid.UUID,
    req: UpdateFormRequest,
    _: dict = Depends(require_permissions(Permissions.UPDATE_FORM)),
    db: AsyncSession = Depends(get_db),
):
    service = FormService(db)
    form = await service.update_form(id, req)
    return SuccessResponse.create(
        data=FormResponse.model_validate(form),
        message="Cập nhật form thành công",
    )


@router.delete(
    "/{id}",
    response_model=SuccessResponse[None],
    summary="Xóa form",
)
async def delete_form(
    id: uuid.UUID,
    _: dict = Depends(require_permissions(Permissions.DELETE_FORM)),
    db: AsyncSession = Depends(get_db),
):
    service = FormService(db)
    await service.delete_form(id)
    return SuccessResponse.create(data=None, message="Xóa form thành công")
