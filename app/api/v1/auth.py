from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.schemas.auth import (
    CurrentUserResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.response import SuccessResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=SuccessResponse[TokenResponse],
    summary="Đăng nhập và nhận JWT",
)
async def login(
    req: LoginRequest, db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    token = await service.login(req)
    return SuccessResponse.create(
        data=TokenResponse(accessToken=token),
        message="Đăng nhập thành công",
    )


@router.post(
    "/register",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới",
)
async def register(
    req: RegisterRequest, db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    user = await service.register(req)
    return SuccessResponse.create(
        data=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            isActive=user.is_active,
        ),
        message="Đăng ký thành công",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/me",
    response_model=SuccessResponse[CurrentUserResponse],
    summary="Lấy thông tin tài khoản hiện tại kèm quyền",
)
async def get_me(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    profile = await service.get_current_user_profile(current_user["sub"])
    return SuccessResponse.create(
        data=profile, message="Lấy thông tin thành công"
    )
