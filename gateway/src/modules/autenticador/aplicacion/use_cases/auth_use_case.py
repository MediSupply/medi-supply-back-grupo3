from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.aplicacion.servicios.auth_service import AuthService


class AuthUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def execute(self, email: str, password: str) -> SessionDto:
        user = self.auth_service.login(email, password)
        if user:
            return user
        else:
            return None

    def signUp(self, name: str, email: str, password: str, role: str = "USER") -> SessionDto:
        """Sign up a new user"""
        return self.auth_service.signUp(name, email, password, role)

    def signOut(self) -> SessionDto:
        """Sign out the current user"""
        return self.auth_service.signOut()
