"""
Entidades del dominio del módulo de autorización refactorizado.
"""

from .resource import AccessRequest, ActionType, ResourceType, RolePermissions
from .token_payload import Role, TokenPayload

__all__ = ["TokenPayload", "Role", "ResourceType", "ActionType", "AccessRequest", "RolePermissions"]
