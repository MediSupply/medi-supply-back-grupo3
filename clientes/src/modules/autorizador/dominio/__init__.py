"""
Dominio del módulo de autorización refactorizado.
"""

from .entities import AccessRequest, ActionType, ResourceType, Role, RolePermissions, TokenPayload
from .exceptions import (
    AuthorizationError,
    ExpiredTokenError,
    InsufficientPermissionsError,
    InvalidTokenError,
    MissingTokenError,
)

__all__ = [
    # Entidades
    "TokenPayload",
    "Role",
    "ResourceType",
    "ActionType",
    "AccessRequest",
    "RolePermissions",
    # Excepciones
    "AuthorizationError",
    "InvalidTokenError",
    "ExpiredTokenError",
    "InsufficientPermissionsError",
    "MissingTokenError",
]
