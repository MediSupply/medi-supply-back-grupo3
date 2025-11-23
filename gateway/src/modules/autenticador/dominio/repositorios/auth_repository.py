from abc import ABC, abstractmethod
from typing import Optional

from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.dominio.entities.user import User


class AuthRepository(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> LoginResultDto: ...

    @abstractmethod
    def signUp(self, name: str, email: str, password: str, role: str = "USER") -> SessionDto: ...

    @abstractmethod
    def signOut(self) -> SessionDto: ...

    @abstractmethod
    def user_exists(self, email: str) -> bool: ...

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]: ...
