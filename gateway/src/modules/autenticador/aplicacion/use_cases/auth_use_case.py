from typing import Optional

from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.aplicacion.servicios.auth_service import AuthService
from modules.autenticador.dominio.entities.user import User


class AuthUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def execute(self, email: str, password: str) -> LoginResultDto:
        return self.auth_service.login(email, password)

    def signUp(self, name: str, email: str, password: str, role: str = "USER") -> SessionDto:
        """Sign up a new user"""
        return self.auth_service.signUp(name, email, password, role)

    def signOut(self) -> SessionDto:
        """Sign out the current user"""
        return self.auth_service.signOut()

    def user_exists(self, email: str) -> bool:
        """Check if a user with the given email already exists"""
        return self.auth_service.user_exists(email)

    def get_current_user(self, token: str) -> Optional[User]:
        """Get current authenticated user from token"""
        return self.auth_service.get_current_user(token)
