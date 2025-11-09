"""
Tests unitarios para el servicio de autenticación del gateway
"""

import os
import sys
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestAuthService:
    """Tests para el servicio de autenticación"""

    def test_auth_service_initialization(self):
        """Test de inicialización del AuthService"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        assert service.secret_key == "secret_key"
        assert service.algorithm == "HS256"
        assert service.auth_repository == mock_repo

    def test_auth_service_login(self):
        """Test del método login del AuthService"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del repositorio
        mock_session = SessionDto(
            id="session-id", user_id="user-id", token="jwt-token", expires_at=datetime.now() + timedelta(hours=1)
        )
        mock_repo.login.return_value = mock_session

        # Test login
        result = service.login("test@example.com", "password123")

        assert result == mock_session
        mock_repo.login.assert_called_once_with("test@example.com", "password123")

    def test_auth_service_login_failure(self):
        """Test del método login cuando falla"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del repositorio que retorna None
        mock_repo.login.return_value = None

        # Test login fallido
        result = service.login("test@example.com", "wrong_password")

        assert result is None
        mock_repo.login.assert_called_once_with("test@example.com", "wrong_password")

    def test_auth_service_signup(self):
        """Test del método signUp del AuthService"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del repositorio
        mock_session = SessionDto(
            id="session-id", user_id="user-id", token="jwt-token", expires_at=datetime.now() + timedelta(hours=1)
        )
        mock_repo.signUp.return_value = mock_session

        # Test signUp
        result = service.signUp("Test User", "test@example.com", "password123", "USER")

        assert result == mock_session
        mock_repo.signUp.assert_called_once_with("Test User", "test@example.com", "password123", "USER")

    def test_auth_service_signup_default_role(self):
        """Test del método signUp con rol por defecto"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del repositorio
        mock_session = SessionDto(
            id="session-id", user_id="user-id", token="jwt-token", expires_at=datetime.now() + timedelta(hours=1)
        )
        mock_repo.signUp.return_value = mock_session

        # Test signUp sin especificar rol (debe usar USER por defecto)
        result = service.signUp("Test User", "test@example.com", "password123")

        assert result == mock_session
        mock_repo.signUp.assert_called_once_with("Test User", "test@example.com", "password123", "USER")

    def test_auth_service_signup_failure(self):
        """Test del método signUp cuando falla"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del repositorio que retorna None
        mock_repo.signUp.return_value = None

        # Test signUp fallido
        result = service.signUp("Test User", "existing@example.com", "password123")

        assert result is None
        mock_repo.signUp.assert_called_once_with("Test User", "existing@example.com", "password123", "USER")

    def test_auth_service_signout(self):
        """Test del método signOut del AuthService"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del repositorio
        mock_session = SessionDto(id="", user_id="", token="", expires_at=datetime.now())
        mock_repo.signOut.return_value = mock_session

        # Test signOut
        result = service.signOut()

        assert result == mock_session
        mock_repo.signOut.assert_called_once()

    def test_auth_service_signout_failure(self):
        """Test del método signOut cuando falla"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del repositorio que retorna None
        mock_repo.signOut.return_value = None

        # Test signOut fallido
        result = service.signOut()

        assert result is None
        mock_repo.signOut.assert_called_once()

    @patch("modules.autenticador.aplicacion.servicios.auth_service.jwt")
    def test_auth_service_get_current_user_success(self, mock_jwt):
        """Test del método get_current_user exitoso"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService
        from modules.autenticador.dominio.entities.user import Role, User

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del token decodificado
        mock_jwt.decode.return_value = {"user_id": "user-id-123", "role": "USER", "exp": 1234567890}

        # Mock del usuario del repositorio
        mock_user = User(
            id="user-id-123",
            name="Test User",
            email="test@example.com",
            password="password123",
            role=Role.USER,
        )
        mock_repo.get_user_by_id.return_value = mock_user

        # Test get_current_user exitoso
        result = service.get_current_user("valid-token")

        assert result is not None
        assert result.id == "user-id-123"
        assert result.name == "Test User"
        assert result.email == "test@example.com"
        mock_jwt.decode.assert_called_once_with("valid-token", "secret_key", algorithms=["HS256"])
        mock_repo.get_user_by_id.assert_called_once_with("user-id-123")

    def test_auth_service_get_current_user_expired_token(self):
        """Test del método get_current_user con token expirado"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService
        import jwt

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Test get_current_user con token expirado usando un token real expirado
        # O simplemente mockear el decode para que lance la excepción
        with patch.object(jwt, 'decode', side_effect=jwt.ExpiredSignatureError("Token expired")):
            result = service.get_current_user("expired-token")

        assert result is None
        mock_repo.get_user_by_id.assert_not_called()

    def test_auth_service_get_current_user_invalid_token(self):
        """Test del método get_current_user con token inválido"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService
        import jwt

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Test get_current_user con token inválido
        with patch.object(jwt, 'decode', side_effect=jwt.InvalidTokenError("Invalid token")):
            result = service.get_current_user("invalid-token")

        assert result is None
        mock_repo.get_user_by_id.assert_not_called()

    @patch("modules.autenticador.aplicacion.servicios.auth_service.jwt")
    def test_auth_service_get_current_user_no_user_id(self, mock_jwt):
        """Test del método get_current_user cuando el token no tiene user_id"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del token sin user_id
        mock_jwt.decode.return_value = {"role": "USER", "exp": 1234567890}

        # Test get_current_user sin user_id
        result = service.get_current_user("token-without-user-id")

        assert result is None
        mock_repo.get_user_by_id.assert_not_called()

    @patch("modules.autenticador.aplicacion.servicios.auth_service.jwt")
    def test_auth_service_get_current_user_not_found(self, mock_jwt):
        """Test del método get_current_user cuando el usuario no existe"""
        from modules.autenticador.aplicacion.servicios.auth_service import AuthService

        mock_repo = Mock()
        service = AuthService(mock_repo, "secret_key", "HS256")

        # Mock del token decodificado
        mock_jwt.decode.return_value = {"user_id": "nonexistent-id", "role": "USER", "exp": 1234567890}

        # Mock del repositorio que retorna None
        mock_repo.get_user_by_id.return_value = None

        # Test get_current_user con usuario inexistente
        result = service.get_current_user("valid-token")

        assert result is None
        mock_repo.get_user_by_id.assert_called_once_with("nonexistent-id")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
