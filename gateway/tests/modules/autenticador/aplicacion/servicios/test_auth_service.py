"""
Tests unitarios para el servicio de autenticación del gateway
"""

import os
import sys
from datetime import datetime, timedelta
from unittest.mock import Mock

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
            id="session-id",
            user_id="user-id",
            token="jwt-token",
            expires_at=datetime.now() + timedelta(hours=1),
            isAdmin=False,
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
            id="session-id",
            user_id="user-id",
            token="jwt-token",
            expires_at=datetime.now() + timedelta(hours=1),
            isAdmin=False,
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
            id="session-id",
            user_id="user-id",
            token="jwt-token",
            expires_at=datetime.now() + timedelta(hours=1),
            isAdmin=False,
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
        mock_session = SessionDto(id="", user_id="", token="", expires_at=datetime.now(), isAdmin=False)
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
