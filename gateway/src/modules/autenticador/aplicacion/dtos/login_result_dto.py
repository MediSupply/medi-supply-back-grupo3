from dataclasses import dataclass
from typing import Optional

from modules.autenticador.aplicacion.dtos.session_dto import SessionDto


@dataclass
class LoginResultDto:
    """DTO para el resultado del login que incluye información sobre el tipo de error"""

    session: Optional[SessionDto]
    user_not_found: bool = False
    invalid_credentials: bool = False

    @classmethod
    def success(cls, session: SessionDto) -> "LoginResultDto":
        """Crear un resultado exitoso"""
        return cls(session=session, user_not_found=False, invalid_credentials=False)

    @classmethod
    def user_not_found_error(cls) -> "LoginResultDto":
        """Crear un resultado de error cuando el usuario no existe"""
        return cls(session=None, user_not_found=True, invalid_credentials=False)

    @classmethod
    def invalid_credentials_error(cls) -> "LoginResultDto":
        """Crear un resultado de error cuando las credenciales son incorrectas"""
        return cls(session=None, user_not_found=False, invalid_credentials=True)
