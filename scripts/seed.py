import asyncio
from sqlalchemy import select

from app.core.constants import Permissions
from app.core.enums import RoleType
from app.core.security import hash_password
from app.db.models import (
    Permission,
    Role,
    RolePermission,
    User,
    UserRole,
)
from app.db.session import AsyncSessionLocal


async def seed_data():
    async with AsyncSessionLocal() as session:
        try:
            permission_map: dict[str, Permission] = {}
            for perm_name in Permissions.get_all():
                stmt = select(Permission).where(Permission.name == perm_name)
                result = await session.execute(stmt)
                perm = result.scalar_one_or_none()

                if not perm:
                    perm = Permission(
                        name=perm_name,
                        display_name=f"Quyền {perm_name}",
                        description=f"Cho phép thực hiện hành động {perm_name}",
                    )
                    session.add(perm)
                    await session.flush()
                permission_map[perm_name] = perm

            roles: dict[str, Role] = {}
            for role_name in [RoleType.ADMIN.value, RoleType.EMPLOYEE.value]:
                stmt = select(Role).where(Role.name == role_name)
                result = await session.execute(stmt)
                role = result.scalar_one_or_none()

                if not role:
                    role = Role(name=role_name)
                    session.add(role)
                    await session.flush()
                roles[role_name] = role

            admin_role = roles[RoleType.ADMIN.value]
            for perm in permission_map.values():
                stmt = select(RolePermission).where(
                    RolePermission.role_id == admin_role.id,
                    RolePermission.permission_id == perm.id,
                )
                if not (await session.execute(stmt)).scalar_one_or_none():
                    session.add(
                        RolePermission(
                            role_id=admin_role.id, permission_id=perm.id
                        )
                    )

            employee_role = roles[RoleType.EMPLOYEE.value]
            employee_permissions = [
                Permissions.VIEW_FORM,
                Permissions.SUBMIT_FORM,
                Permissions.VIEW_SUBMISSIONS,
            ]
            for perm_name in employee_permissions:
                if perm_name in permission_map:
                    perm = permission_map[perm_name]
                    stmt = select(RolePermission).where(
                        RolePermission.role_id == employee_role.id,
                        RolePermission.permission_id == perm.id,
                    )
                    if not (await session.execute(stmt)).scalar_one_or_none():
                        session.add(
                            RolePermission(
                                role_id=employee_role.id,
                                permission_id=perm.id,
                            )
                        )

            admin_email = "admin@gmail.com"
            stmt = select(User).where(User.email == admin_email)
            admin_user = (await session.execute(stmt)).scalar_one_or_none()

            if not admin_user:
                admin_user = User(
                    username="admin",
                    email=admin_email,
                    password_hash=hash_password("123456"),
                    is_active=True,
                )
                session.add(admin_user)
                await session.flush()

                session.add(
                    UserRole(user_id=admin_user.id, role_id=admin_role.id)
                )

            await session.commit()
            print("Seed data completed successfully")

        except Exception as e:
            await session.rollback()
            print(f"Error seeding data: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_data())
