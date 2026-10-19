import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import require_permissions
from app.core.constants import Permissions
from app.db.session import get_db
from app.schemas.field import (
    AddFieldRequest,
    FieldResponse,
    UpdateFieldOrdersRequest,
    UpdateFieldRequest,
)
from app.schemas.response import SuccessResponse
from app.services.field_service import FieldService

router = APIRouter(prefix="/forms/{form_id}/fields", tags=["Fields"])


@router.post(
    "",
    response_model=SuccessResponse[FieldResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Thêm field mới vào form",
)
async def add_field(
    form_id: uuid.UUID,
    req: AddFieldRequest,
    _: dict = Depends(require_permissions(Permissions.CREATE_FIELD)),
    db: AsyncSession = Depends(get_db),
):
    service = FieldService(db)
    field = await service.add_field(form_id, req)
    return SuccessResponse.create(
        data=FieldResponse.model_validate(field),
        message="Thêm field thành công",
        status_code=status.HTTP_201_CREATED,
    )


@router.put(
    "/order",
    response_model=SuccessResponse[None],
    summary="Cập nhật thứ tự sắp xếp của nhiều field",
)
async def update_field_orders(
    form_id: uuid.UUID,
    req: UpdateFieldOrdersRequest,
    _: dict = Depends(require_permissions(Permissions.UPDATE_FIELD)),
    db: AsyncSession = Depends(get_db),
):
    service = FieldService(db)
    orders_data = [item.model_dump() for item in req.orders]
    await service.update_field_orders(form_id, orders_data)
    return SuccessResponse.create(
        data=None, message="Cập nhật thứ tự field thành công"
    )


@router.put(
    "/{field_id}",
    response_model=SuccessResponse[FieldResponse],
    summary="Cập nhật field",
)
async def update_field(
    form_id: uuid.UUID,
    field_id: uuid.UUID,
    req: UpdateFieldRequest,
    _: dict = Depends(require_permissions(Permissions.UPDATE_FIELD)),
    db: AsyncSession = Depends(get_db),
):
    service = FieldService(db)
    field = await service.update_field(form_id, field_id, req)
    return SuccessResponse.create(
        data=FieldResponse.model_validate(field),
        message="Cập nhật field thành công",
    )


@router.delete(
    "/{field_id}",
    response_model=SuccessResponse[None],
    summary="Xóa field",
)
async def delete_field(
    form_id: uuid.UUID,
    field_id: uuid.UUID,
    _: dict = Depends(require_permissions(Permissions.DELETE_FIELD)),
    db: AsyncSession = Depends(get_db),
):
    service = FieldService(db)
    await service.delete_field(form_id, field_id)
    return SuccessResponse.create(data=None, message="Xóa field thành công")
