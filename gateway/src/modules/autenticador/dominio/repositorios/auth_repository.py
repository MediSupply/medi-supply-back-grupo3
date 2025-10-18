from abc import ABC, abstractmethod

from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto


class AuthRepository(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> LoginResultDto: ...

    @abstractmethod
    def signUp(self, name: str, email: str, password: str, role: str = "USER") -> SessionDto: ...

    @abstractmethod
    def signOut(self) -> SessionDto: ...

    @abstractmethod
    def user_exists(self, email: str) -> bool: ...
