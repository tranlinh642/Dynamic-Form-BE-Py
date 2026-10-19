from datetime import datetime, timezone
import math
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel):
    success: bool
    statusCode: int
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    message: str


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    totalPages: int


class SuccessResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None
    meta: Optional[Any] = None

    @classmethod
    def create(
        cls,
        data: Optional[T] = None,
        message: str = "Thành công",
        status_code: int = 200,
        meta: Optional[Any] = None,
    ) -> "SuccessResponse[T]":
        return cls(
            success=True,
            statusCode=status_code,
            message=message,
            data=data,
            meta=meta,
        )


class PaginatedResponse(BaseResponse, Generic[T]):
    data: List[T]
    meta: PaginationMeta

    @classmethod
    def create(
        cls,
        data: List[T],
        total: int,
        page: int,
        limit: int,
        message: str = "Thành công",
    ) -> "PaginatedResponse[T]":
        total_pages = math.ceil(total / limit) if limit > 0 else 0
        return cls(
            success=True,
            statusCode=200,
            message=message,
            data=data,
            meta=PaginationMeta(
                total=total,
                page=page,
                limit=limit,
                totalPages=total_pages,
            ),
        )


class ErrorResponse(BaseResponse):
    errorCode: str
    errors: Optional[List[Any]] = None
