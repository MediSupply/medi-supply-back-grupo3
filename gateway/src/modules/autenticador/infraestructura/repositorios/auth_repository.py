import uuid
from datetime import datetime, timedelta

import jwt
from config.db import db
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper
from modules.autenticador.dominio.entities.session import Session
from modules.autenticador.dominio.repositorios.auth_repository import AuthRepository
from modules.autenticador.infraestructura.dto.user import Role
from modules.autenticador.infraestructura.dto.user import User as UserModel


class AuthRepositoryImpl(AuthRepository):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def login(self, email: str, password: str) -> SessionDto:
        try:
            # Query the database using the correct model
            auth = db.session.query(UserModel).filter_by(email=email).first()
            if auth and auth.password == password:  # Add password verification
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
                return SessionMapper.entity_to_dto(session)
            else:
                return None
        except Exception as e:
            print(f"Error in login: {e}")  # Add logging for debugging
            return None

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
