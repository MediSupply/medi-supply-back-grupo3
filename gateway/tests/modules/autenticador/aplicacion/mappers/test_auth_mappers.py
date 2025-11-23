"""
Tests unitarios para los mappers del módulo de autenticación del gateway
"""

import os
import sys
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestSessionMapper:
    """Tests para el SessionMapper"""

    def test_session_mapper_entity_to_dto(self):
        """Test del método entity_to_dto del SessionMapper"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper
        from modules.autenticador.dominio.entities.session import Session

        expires_at = datetime.now() + timedelta(hours=1)
        session = Session(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at, isAdmin=False)

        session_dto = SessionMapper.entity_to_dto(session)
        assert isinstance(session_dto, SessionDto)
        assert session_dto.id == "session-id"
        assert session_dto.user_id == "user-id"
        assert session_dto.token == "jwt-token"
        assert session_dto.expires_at == expires_at
        assert session_dto.isAdmin == False

    def test_session_mapper_dto_to_entity(self):
        """Test del método dto_to_entity del SessionMapper"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper
        from modules.autenticador.dominio.entities.session import Session

        expires_at = datetime.now() + timedelta(hours=1)
        session_dto = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at, isAdmin=True)

        session = SessionMapper.dto_to_entity(session_dto)
        assert isinstance(session, Session)
        assert session.id == "session-id"
        assert session.user_id == "user-id"
        assert session.token == "jwt-token"
        assert session.expires_at == expires_at
        assert session.isAdmin == True

    def test_session_mapper_dto_to_json(self):
        """Test del método dto_to_json del SessionMapper"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper

        expires_at = datetime.now() + timedelta(hours=1)
        session_dto = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at, isAdmin=False)

        json_data = SessionMapper.dto_to_json(session_dto)
        assert isinstance(json_data, dict)
        assert json_data["id"] == "session-id"
        assert json_data["user_id"] == "user-id"
        assert json_data["token"] == "jwt-token"
        assert json_data["expires_at"] == expires_at
        assert json_data["isAdmin"] == False

    def test_session_mapper_json_to_dto(self):
        """Test del método json_to_dto del SessionMapper"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper

        expires_at = datetime.now() + timedelta(hours=1)
        json_data = {"id": "session-id", "user_id": "user-id", "token": "jwt-token", "expires_at": expires_at, "isAdmin": True}

        session_dto = SessionMapper.json_to_dto(json_data)
        assert isinstance(session_dto, SessionDto)
        assert session_dto.id == "session-id"
        assert session_dto.user_id == "user-id"
        assert session_dto.token == "jwt-token"
        assert session_dto.expires_at == expires_at
        assert session_dto.isAdmin == True


class TestUserMapper:
    """Tests para el UserMapper"""

    def test_user_mapper_entity_to_dto(self):
        """Test del método entity_to_dto del UserMapper"""
        from modules.autenticador.aplicacion.dtos.user_dto import UserDto
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper
        from modules.autenticador.dominio.entities.user import Role, User

        user = User(id="user-id", name="Test User", email="test@example.com", password="password123", role=Role.USER)

        user_dto = UserMapper.entity_to_dto(user)
        assert isinstance(user_dto, UserDto)
        assert user_dto.id == "user-id"
        assert user_dto.name == "Test User"
        assert user_dto.email == "test@example.com"
        assert user_dto.password == "password123"
        assert user_dto.role.value == "user"  # DTO usa minúsculas
        assert user_dto.token == ""  # Token is not part of domain entity

    def test_user_mapper_dto_to_entity(self):
        """Test del método dto_to_entity del UserMapper"""
        from modules.autenticador.aplicacion.dtos.user_dto import RoleDto, UserDto
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper
        from modules.autenticador.dominio.entities.user import User

        user_dto = UserDto(
            id="user-id",
            name="Test User",
            email="test@example.com",
            password="password123",
            role=RoleDto.USER,  # DTO usa minúsculas
            token="jwt-token",
        )

        user = UserMapper.dto_to_entity(user_dto)
        assert isinstance(user, User)
        assert user.id == "user-id"
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.role.value == "USER"  # Domain usa mayúsculas

    def test_user_mapper_role_conversion(self):
        """Test de conversión de roles entre entidad y DTO"""
        from modules.autenticador.aplicacion.dtos.user_dto import RoleDto, UserDto
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper
        from modules.autenticador.dominio.entities.user import Role, User

        # Test USER role
        user = User(id="user-id", name="Test User", email="test@example.com", password="password123", role=Role.USER)

        user_dto = UserMapper.entity_to_dto(user)
        assert user_dto.role == RoleDto.USER  # DTO usa minúsculas

        # Test ADMIN role
        admin_user = User(id="admin-id", name="Admin User", email="admin@example.com", password="admin123", role=Role.ADMIN)

        admin_dto = UserMapper.entity_to_dto(admin_user)
        assert admin_dto.role == RoleDto.ADMIN  # DTO usa minúsculas

    def test_user_mapper_json_to_dto(self):
        """Test del método json_to_dto del UserMapper"""
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper

        json_data = {
            "id": "user-id",
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "role": "user",
            "token": "jwt-token",
        }

        user_dto = UserMapper.json_to_dto(json_data)
        assert user_dto.id == "user-id"
        assert user_dto.name == "Test User"
        assert user_dto.email == "test@example.com"
        assert user_dto.password == "password123"
        assert user_dto.role.value == "user"
        assert user_dto.token == "jwt-token"

    def test_user_mapper_dto_to_json(self):
        """Test del método dto_to_json del UserMapper"""
        from modules.autenticador.aplicacion.dtos.user_dto import RoleDto, UserDto
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper

        user_dto = UserDto(
            id="user-id",
            name="Test User",
            email="test@example.com",
            password="password123",
            role=RoleDto.USER,
            token="jwt-token",
        )

        json_data = UserMapper.dto_to_json(user_dto)
        assert json_data["id"] == "user-id"
        assert json_data["name"] == "Test User"
        assert json_data["email"] == "test@example.com"
        assert json_data["password"] == "password123"
        assert json_data["role"] == "user"
        assert json_data["token"] == "jwt-token"

    def test_user_mapper_entity_to_json_safe(self):
        """Test del método entity_to_json_safe del UserMapper"""
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper
        from modules.autenticador.dominio.entities.user import Role, User

        user = User(id="user-id", name="Test User", email="test@example.com", password="password123", role=Role.USER)

        json_data = UserMapper.entity_to_json_safe(user)
        assert json_data["id"] == "user-id"
        assert json_data["name"] == "Test User"
        assert json_data["email"] == "test@example.com"
        assert json_data["role"] == "user"  # Lowercase
        assert "password" not in json_data  # Password no debe estar en el JSON seguro

    def test_user_mapper_infrastructure_to_domain(self):
        """Test del método infrastructure_to_domain del UserMapper"""
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper
        from modules.autenticador.dominio.entities.user import Role, User
        from modules.autenticador.infraestructura.dto.user import Role as InfraRole
        from modules.autenticador.infraestructura.dto.user import User as InfraUser

        # Crear un mock de infraestructura user
        infra_user = Mock()
        infra_user.id = "user-id"
        infra_user.name = "Test User"
        infra_user.email = "test@example.com"
        infra_user.password = "password123"
        infra_user.role = Mock()
        infra_user.role.value = "USER"

        domain_user = UserMapper.infrastructure_to_domain(infra_user)
        assert isinstance(domain_user, User)
        assert domain_user.id == "user-id"
        assert domain_user.name == "Test User"
        assert domain_user.email == "test@example.com"
        assert domain_user.password == "password123"
        assert domain_user.role == Role.USER

    def test_user_mapper_domain_to_infrastructure(self):
        """Test del método domain_to_infrastructure del UserMapper"""
        from modules.autenticador.aplicacion.mappers.user_mapper import UserMapper
        from modules.autenticador.dominio.entities.user import Role, User

        domain_user = User(id="user-id", name="Test User", email="test@example.com", password="password123", role=Role.USER)

        infra_user = UserMapper.domain_to_infrastructure(domain_user)
        assert infra_user.id == "user-id"
        assert infra_user.name == "Test User"
        assert infra_user.email == "test@example.com"
        assert infra_user.password == "password123"
        assert infra_user.role.value == "USER"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
