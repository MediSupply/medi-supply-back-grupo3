import uuid
from datetime import datetime, timedelta
from typing import Optional

import jwt
from config.db import db
from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper
from modules.autenticador.dominio.entities.session import Session
from modules.autenticador.dominio.entities.user import User
from modules.autenticador.dominio.repositorios.auth_repository import AuthRepository
from modules.autenticador.infraestructura.dto.user import Role
from modules.autenticador.infraestructura.dto.user import User as UserModel


class AuthRepositoryImpl(AuthRepository):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def login(self, email: str, password: str) -> LoginResultDto:
        try:
            # Query the database using the correct model
            auth = db.session.query(UserModel).filter_by(email=email).first()

            # Si el usuario no existe
            if not auth:
                return LoginResultDto.user_not_found_error()

            # Si el usuario existe pero la contraseña es incorrecta
            if auth.password != password:
                return LoginResultDto.invalid_credentials_error()

            # Si todo está correcto, crear la sesión
            exp = datetime.now() + timedelta(hours=1)
            token = jwt.encode(
                {"user_id": auth.id, "role": auth.role.value, "exp": exp}, key=self.secret_key, algorithm=self.algorithm
            )

            session = Session(
                id=auth.id,
                user_id=auth.id,
                token=token,
                expires_at=exp,
            )
            return LoginResultDto.success(SessionMapper.entity_to_dto(session))

        except Exception as e:
            print(f"Error in login: {e}")  # Add logging for debugging
            return LoginResultDto.invalid_credentials_error()

    def signUp(self, name: str, email: str, password: str, role: str = "USER") -> SessionDto:
        try:
            # Check if user already exists
            existing_user = db.session.query(UserModel).filter_by(email=email).first()
            if existing_user:
                print(f"User with email {email} already exists")
                return None

            # Generate unique user ID
            user_id = str(uuid.uuid4())

            # Convert role string to Role enum
            user_role = Role.USER if role.upper() == "USER" else Role.ADMIN

            # Create new user
            new_user = UserModel(id=user_id, name=name, email=email, password=password, role=user_role)

            # Add to database
            db.session.add(new_user)
            db.session.commit()

            # Generate JWT token
            exp = datetime.now() + timedelta(hours=1)
            token = jwt.encode(
                {"user_id": user_id, "role": user_role.value, "exp": exp}, key=self.secret_key, algorithm=self.algorithm
            )

            # Create session
            session = Session(
                id=user_id,
                user_id=user_id,
                token=token,
                expires_at=exp,
            )

            return SessionMapper.entity_to_dto(session)

        except Exception as e:
            print(f"Error in signUp: {e}")
            db.session.rollback()
            return None

    def signOut(self) -> SessionDto:
        try:
            # For JWT-based authentication, logout is typically handled client-side
            # by removing the token from storage. Since JWT is stateless,
            # we don't need to invalidate the token on the server.
            # We can return a simple success response or None to indicate successful logout.

            # Create an empty session to indicate successful logout
            logout_session = Session(
                id="",  # Empty ID for logout
                user_id="",  # Empty user_id for logout
                token="",  # Empty token for logout
                expires_at=datetime.now(),  # Current time to indicate expired
            )

            return SessionMapper.entity_to_dto(logout_session)

        except Exception as e:
            print(f"Error in signOut: {e}")
            return None

    def user_exists(self, email: str) -> bool:
        """Check if a user with the given email already exists"""
        try:
            existing_user = db.session.query(UserModel).filter_by(email=email).first()
            return existing_user is not None
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return False

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID from the database"""
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper

        try:
            user_model = db.session.query(UserModel).filter_by(id=user_id).first()
            if not user_model:
                return None
            # Convert infrastructure model to domain entity
            return UserMapper.infrastructure_to_domain(user_model)
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
