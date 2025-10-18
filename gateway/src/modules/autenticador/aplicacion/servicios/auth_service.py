from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.dominio.repositorios.auth_repository import AuthRepository


class AuthService:
    def __init__(self, auth_repository: AuthRepository, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.auth_repository = auth_repository

    def login(self, email: str, password: str) -> SessionDto:
        """Login using the repository to query the database"""
        return self.auth_repository.login(email, password)

    def signUp(self, name: str, email: str, password: str, role: str = "USER") -> SessionDto:
        """Sign up a new user using the repository"""
        return self.auth_repository.signUp(name, email, password, role)

    def signOut(self) -> SessionDto:
        """Sign out the current user"""
        return self.auth_repository.signOut()

    def user_exists(self, email: str) -> bool:
        """Check if a user with the given email already exists"""
        return self.auth_repository.user_exists(email)
