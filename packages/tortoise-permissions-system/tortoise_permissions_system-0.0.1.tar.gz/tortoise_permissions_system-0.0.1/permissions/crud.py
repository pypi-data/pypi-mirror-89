from typing import Optional, List
from tortoise.query_utils import Q

from backend.common.crud import CRUDBase

from permissions.enums import Permissions, Roles
from permissions.models import AccountRole, Permission, Role, RolePermission
from permissions.schemas import (
    AccountRoleCreate, AccountRoleUpdate,
    PermissionCreate, PermissionUpdate,
    RoleCreate, RoleUpdate, RolePermissionUpdate, RolePermissionCreate
)


class CRUDAccountRole(CRUDBase[AccountRole, AccountRoleCreate, AccountRoleUpdate]):

    async def get_by_account(self, account_id: int) -> Optional[AccountRole]:
        return await self.model.get_or_none(account_id=account_id)


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):

    async def get_by_permission(self, permission_type: Permissions) -> Optional[Permission]:
        return await self.model.get_or_none(name=permission_type)

    async def get_all_permissions(self) -> List[Permission]:
        """Получение списка всех пермишенов в системе."""
        return await self.model.all()


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    async def get_by_role(self, role_type: Roles) -> Optional[Role]:
        return await self.model.get_or_none(name=role_type)

    async def get_all_roles(self) -> List[dict]:
        """
        Получение списка всех ролей в системе.
        В словарях хранится форма {'id': 1, 'name': 'CUSTOMER', 'description': 'Клиент'}
        """
        return await self.model.all()


class CRUDRolePermission(CRUDBase[RolePermission, RolePermissionCreate, RolePermissionUpdate]):

    async def get_by_role(self, role_id: int) -> List[dict]:
        return await self.model.get_or_none(role_id=role_id)

    async def get_by_role_and_permission(self, role_id: int, permission_id: int) -> Optional[RolePermission]:
        query = (
            Q(
                Q(role_id=role_id),
                Q(permission_id=permission_id),
                join_type='AND'
            )
        )
        return await self.model.filter(query).first()


role = CRUDRole(Role)
permission = CRUDPermission(Permission)
account_role = CRUDAccountRole(AccountRole)
role_permission = CRUDRolePermission(RolePermission)
