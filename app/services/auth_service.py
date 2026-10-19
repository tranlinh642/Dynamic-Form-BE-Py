import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import RoleType
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User, UserRole
from app.db.repositories.role_repository import RoleRepository
from app.db.repositories.user_repository import UserRepository
from app.schemas.auth import CurrentUserResponse, LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.role_repo = RoleRepository(session)

    async def register(self, req: RegisterRequest) -> User:
        existing_email = await self.user_repo.get_by_email(req.email)
        if existing_email:
            raise BadRequestException("Email đã được sử dụng")

        existing_username = await self.user_repo.get_by_username(req.username)
        if existing_username:
            raise BadRequestException("Tên đăng nhập đã được sử dụng")

        default_role = await self.role_repo.get_by_name(RoleType.EMPLOYEE.value)
        if not default_role:
            default_role = await self.role_repo.get_by_name(RoleType.ADMIN.value)

        new_user = User(
            username=req.username,
            email=req.email,
            password_hash=hash_password(req.password),
            is_active=True,
        )
        created_user = await self.user_repo.create(new_user)

        if default_role:
            user_role = UserRole(
                user_id=created_user.id, role_id=default_role.id
            )
            self.session.add(user_role)
            await self.session.flush()

        return created_user

    async def login(self, req: LoginRequest) -> str:
        user = await self.user_repo.get_by_username(req.username)
        if not user:
            raise UnauthorizedException("Sai tài khoản hoặc mật khẩu")

        if not verify_password(req.password, user.password_hash):
            raise UnauthorizedException("Sai tài khoản hoặc mật khẩu")

        if not user.is_active:
            raise UnauthorizedException("Tài khoản đã bị vô hiệu hóa")

        permissions = await self.user_repo.get_permissions_by_user_id(user.id)

        token_payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "permissions": permissions,
        }
        return create_access_token(token_payload)

    async def get_current_user_profile(
        self, user_id: uuid.UUID | str
    ) -> CurrentUserResponse:
        user = await self.user_repo.get_user_with_roles(user_id)
        if not user:
            raise UnauthorizedException("Không tìm thấy người dùng")

        roles = [ur.role.name for ur in user.user_roles if ur.role]
        permissions = await self.user_repo.get_permissions_by_user_id(user.id)

        return CurrentUserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            isActive=user.is_active,
            roles=roles,
            permissions=permissions,
        )
