"""
Tests unitarios para los DTOs del módulo de autenticación del gateway
"""

import os
import sys
from datetime import datetime, timedelta

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestSessionDto:
    """Tests para el SessionDto"""

    def test_session_dto_creation(self):
        """Test de creación del SessionDto"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto

        expires_at = datetime.now() + timedelta(hours=1)
        session_dto = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at)

        assert session_dto.id == "session-id"
        assert session_dto.user_id == "user-id"
        assert session_dto.token == "jwt-token"
        assert session_dto.expires_at == expires_at

    def test_session_dto_immutable(self):
        """Test de que SessionDto es inmutable"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto

        expires_at = datetime.now() + timedelta(hours=1)
        session_dto = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at)

        # Verificar que es inmutable (dataclass frozen)
        with pytest.raises(AttributeError):
            session_dto.id = "new-id"


class TestUserDto:
    """Tests para el UserDto"""

    def test_user_dto_creation(self):
        """Test de creación del UserDto"""
        from modules.autenticador.aplicacion.dtos.user_dto import RoleDto, UserDto

        user_dto = UserDto(
            id="user-id",
            name="Test User",
            email="test@example.com",
            password="password123",
            role=RoleDto.USER,
            token="jwt-token",
        )

        assert user_dto.id == "user-id"
        assert user_dto.name == "Test User"
        assert user_dto.email == "test@example.com"
        assert user_dto.password == "password123"
        assert user_dto.role == RoleDto.USER
        assert user_dto.token == "jwt-token"

    def test_user_dto_admin_role(self):
        """Test de creación de UserDto con rol ADMIN"""
        from modules.autenticador.aplicacion.dtos.user_dto import RoleDto, UserDto

        user_dto = UserDto(
            id="admin-id",
            name="Admin User",
            email="admin@example.com",
            password="admin123",
            role=RoleDto.ADMIN,
            token="admin-token",
        )

        assert user_dto.role == RoleDto.ADMIN

    def test_user_dto_role_enum(self):
        """Test de los valores del enum RoleDto"""
        from modules.autenticador.aplicacion.dtos.user_dto import RoleDto

        assert RoleDto.USER.value == "user"
        assert RoleDto.ADMIN.value == "admin"

    def test_user_dto_immutable(self):
        """Test de que UserDto es inmutable"""
        from modules.autenticador.aplicacion.dtos.user_dto import RoleDto, UserDto

        user_dto = UserDto(
            id="user-id",
            name="Test User",
            email="test@example.com",
            password="password123",
            role=RoleDto.USER,
            token="jwt-token",
        )

        # Verificar que es inmutable
        with pytest.raises(AttributeError):
            user_dto.id = "new-id"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
