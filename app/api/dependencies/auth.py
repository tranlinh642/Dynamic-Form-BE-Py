from typing import Callable, List
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
) -> dict:
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Chưa cung cấp token xác thực")

    token = credentials.credentials
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token đã hết hạn")
    except (jwt.InvalidTokenError, Exception):
        raise UnauthorizedException("Token không hợp lệ")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token không hợp lệ")

    return payload


def require_permissions(*required_perms: str) -> Callable:
    async def permission_checker(
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        user_perms: List[str] = current_user.get("permissions", [])
        for perm in required_perms:
            if perm not in user_perms:
                raise ForbiddenException("Không có quyền truy cập")
        return current_user

    return permission_checker
