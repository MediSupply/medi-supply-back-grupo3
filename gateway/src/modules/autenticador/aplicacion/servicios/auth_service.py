from typing import Optional

import jwt
from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.dominio.entities.user import User
from modules.autenticador.dominio.repositorios.auth_repository import AuthRepository


class AuthService:
    def __init__(self, auth_repository: AuthRepository, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.auth_repository = auth_repository

    def login(self, email: str, password: str) -> LoginResultDto:
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

    def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        try:
            # Decode the JWT token
            decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = decoded_token.get("user_id")
            if not user_id:
                return None
            # Get user from repository
            return self.auth_repository.get_user_by_id(user_id)
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None
        except Exception as e:
            print(f"Error getting current user: {e}")
            return None
