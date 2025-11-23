from dataclasses import dataclass
from enum import Enum

from modules.autorizador.dominio.entities.user import Role


class RoleDto(Enum):
    ADMIN = "ADMIN"
    USER = "USER"


@dataclass(frozen=True)
class UserDto:
    """
    DTO que representa el usuario.
    """

    id: str
    name: str
    email: str
    password: str
    role: RoleDto
    token: str
