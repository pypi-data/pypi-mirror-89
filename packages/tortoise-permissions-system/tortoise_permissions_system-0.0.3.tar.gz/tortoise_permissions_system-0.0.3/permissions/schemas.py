from pydantic import BaseModel

from enum import Enum


class CreateBaseEnum(BaseModel):
    name: Enum
    description: str


class UpdateBase(BaseModel):
    pass


class AccountRoleCreate(BaseModel):
    role_id: int
    account_id: int


class AccountRoleUpdate(UpdateBase):
    pass


class PermissionCreate(CreateBaseEnum):
    pass


class PermissionUpdate(UpdateBase):
    pass


class RoleCreate(CreateBaseEnum):
    pass


class RoleUpdate(UpdateBase):
    pass


class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int


class RolePermissionUpdate(UpdateBase):
    pass
