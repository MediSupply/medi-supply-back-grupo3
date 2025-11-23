"""
Tests unitarios para el repositorio de autenticación del gateway
"""

import os
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestAuthRepositoryImpl:
    """Tests para el AuthRepositoryImpl"""

    def test_auth_repository_initialization(self):
        """Test de inicialización del AuthRepositoryImpl"""
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        repo = AuthRepositoryImpl("secret_key", "HS256")

        assert repo.secret_key == "secret_key"
        assert repo.algorithm == "HS256"

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_login_success(self, mock_db):
        """Test del método login exitoso"""
        from modules.autenticador.infraestructura.dto.user import Role
        from modules.autenticador.infraestructura.dto.user import User as UserModel
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock del usuario en la base de datos
        mock_user = MagicMock()
        mock_user.id = "user-id"
        mock_user.password = "password123"
        mock_user.role = Role.USER

        # Mock de la sesión de base de datos
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test login exitoso
        result = repo.login("test@example.com", "password123")

        assert result is not None
        assert result.session is not None
        assert result.session.id == "user-id"
        assert result.session.user_id == "user-id"
        assert result.session.token is not None
        assert result.session.expires_at is not None
        assert result.session.isAdmin == False  # USER role
        assert result.user_not_found is False
        assert result.invalid_credentials is False

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_login_admin_role(self, mock_db):
        """Test del método login con rol ADMIN"""
        from modules.autenticador.infraestructura.dto.user import Role
        from modules.autenticador.infraestructura.dto.user import User as UserModel
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock del usuario admin en la base de datos
        mock_user = MagicMock()
        mock_user.id = "admin-id"
        mock_user.password = "admin123"
        mock_user.role = Role.ADMIN

        # Mock de la sesión de base de datos
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test login exitoso con rol ADMIN
        result = repo.login("admin@example.com", "admin123")

        assert result is not None
        assert result.session is not None
        assert result.session.id == "admin-id"
        assert result.session.user_id == "admin-id"
        assert result.session.token is not None
        assert result.session.expires_at is not None
        assert result.session.isAdmin == True  # ADMIN role
        assert result.user_not_found is False
        assert result.invalid_credentials is False

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_login_wrong_password(self, mock_db):
        """Test del método login con contraseña incorrecta"""
        from modules.autenticador.infraestructura.dto.user import Role
        from modules.autenticador.infraestructura.dto.user import User as UserModel
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock del usuario en la base de datos
        mock_user = MagicMock()
        mock_user.id = "user-id"
        mock_user.password = "password123"
        mock_user.role = Role.USER

        # Mock de la sesión de base de datos
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test login con contraseña incorrecta
        result = repo.login("test@example.com", "wrong_password")

        assert result is not None
        assert result.session is None
        assert result.user_not_found is False
        assert result.invalid_credentials is True

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_login_user_not_found(self, mock_db):
        """Test del método login cuando el usuario no existe"""
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock de la sesión de base de datos que retorna None
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test login con usuario inexistente
        result = repo.login("nonexistent@example.com", "password123")

        assert result is not None
        assert result.session is None
        assert result.user_not_found is True
        assert result.invalid_credentials is False

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.uuid")
    def test_auth_repository_signup_success(self, mock_uuid, mock_db):
        """Test del método signUp exitoso"""
        from modules.autenticador.infraestructura.dto.user import Role
        from modules.autenticador.infraestructura.dto.user import User as UserModel
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock de UUID
        mock_uuid.uuid4.return_value = "new-user-id"

        # Mock de la sesión de base de datos
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None  # Usuario no existe

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test signUp exitoso
        result = repo.signUp("Test User", "test@example.com", "password123", "USER")

        assert result is not None
        assert result.id == "new-user-id"
        assert result.user_id == "new-user-id"
        assert result.token is not None
        assert result.expires_at is not None
        assert result.isAdmin == False  # USER role

        # Verificar que se agregó el usuario a la base de datos
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_signup_user_exists(self, mock_db):
        """Test del método signUp cuando el usuario ya existe"""
        from modules.autenticador.infraestructura.dto.user import Role
        from modules.autenticador.infraestructura.dto.user import User as UserModel
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock del usuario existente
        mock_user = MagicMock()
        mock_user.id = "existing-user-id"

        # Mock de la sesión de base de datos
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test signUp con usuario existente
        result = repo.signUp("Test User", "existing@example.com", "password123", "USER")

        assert result is None

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.uuid")
    def test_auth_repository_signup_admin_role(self, mock_uuid, mock_db):
        """Test del método signUp con rol ADMIN"""
        from modules.autenticador.infraestructura.dto.user import Role
        from modules.autenticador.infraestructura.dto.user import User as UserModel
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock de UUID
        mock_uuid.uuid4.return_value = "admin-user-id"

        # Mock de la sesión de base de datos
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None  # Usuario no existe

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test signUp con rol ADMIN
        result = repo.signUp("Admin User", "admin@example.com", "admin123", "ADMIN")

        assert result is not None
        assert result.id == "admin-user-id"
        assert result.user_id == "admin-user-id"
        assert result.isAdmin == True  # ADMIN role

    def test_auth_repository_signout(self):
        """Test del método signOut"""
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test signOut
        result = repo.signOut()

        assert result is not None
        assert result.id == ""
        assert result.user_id == ""
        assert result.token == ""
        assert result.expires_at is not None
        assert result.isAdmin == False

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_login_exception(self, mock_db):
        """Test del método login con excepción"""
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock de la sesión de base de datos que lanza excepción
        mock_session = MagicMock()
        mock_session.query.side_effect = Exception("Database error")

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test login con excepción
        result = repo.login("test@example.com", "password123")

        assert result is not None
        assert result.session is None
        assert result.user_not_found is False
        assert result.invalid_credentials is True

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.uuid")
    def test_auth_repository_signup_exception(self, mock_uuid, mock_db):
        """Test del método signUp con excepción"""
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock de UUID
        mock_uuid.uuid4.return_value = "new-user-id"

        # Mock de la sesión de base de datos que lanza excepción
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session.add.side_effect = Exception("Database error")

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test signUp con excepción
        result = repo.signUp("Test User", "test@example.com", "password123", "USER")

        assert result is None
        mock_session.rollback.assert_called_once()

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    @patch("modules.autenticador.aplicacion.mappers.user_mapper.UserMapper")
    def test_auth_repository_get_user_by_id_success(self, mock_mapper_class, mock_db):
        """Test del método get_user_by_id exitoso"""
        from modules.autenticador.dominio.entities.user import Role, User
        from modules.autenticador.infraestructura.dto.user import Role as InfraRole
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock del usuario en la base de datos
        mock_user = MagicMock()
        mock_user.id = "user-id-123"
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_user.password = "password123"
        mock_user.role = InfraRole.USER

        # Mock de la sesión de base de datos
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

        mock_db.session = mock_session

        # Mock del mapper que retorna un User del dominio
        expected_user = User(
            id="user-id-123",
            name="Test User",
            email="test@example.com",
            password="password123",
            role=Role.USER,
        )
        mock_mapper_class.infrastructure_to_domain.return_value = expected_user

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test get_user_by_id exitoso
        result = repo.get_user_by_id("user-id-123")

        assert result is not None
        assert result.id == "user-id-123"
        assert result.name == "Test User"
        assert result.email == "test@example.com"
        assert result.role == Role.USER
        mock_mapper_class.infrastructure_to_domain.assert_called_once_with(mock_user)

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_get_user_by_id_not_found(self, mock_db):
        """Test del método get_user_by_id cuando el usuario no existe"""
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock de la sesión de base de datos que retorna None
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test get_user_by_id con usuario inexistente
        result = repo.get_user_by_id("nonexistent-id")

        assert result is None

    @patch("modules.autenticador.infraestructura.repositorios.auth_repository.db")
    def test_auth_repository_get_user_by_id_exception(self, mock_db):
        """Test del método get_user_by_id con excepción"""
        from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl

        # Mock de la sesión de base de datos que lanza excepción
        mock_session = MagicMock()
        mock_session.query.side_effect = Exception("Database error")

        mock_db.session = mock_session

        repo = AuthRepositoryImpl("secret_key", "HS256")

        # Test get_user_by_id con excepción
        result = repo.get_user_by_id("user-id-123")

        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
