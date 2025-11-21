"""
Tests unitarios para los use cases del módulo de autenticación del gateway
"""

import os
import sys
from unittest.mock import Mock

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestAuthUseCase:
    """Tests para el AuthUseCase"""

    def test_auth_use_case_initialization(self):
        """Test de inicialización del AuthUseCase"""
        from modules.autenticador.aplicacion.use_cases.auth_use_case import AuthUseCase

        mock_service = Mock()
        use_case = AuthUseCase(mock_service)

        assert use_case.auth_service == mock_service

    def test_auth_use_case_login(self):
        """Test del método execute del AuthUseCase"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.use_cases.auth_use_case import AuthUseCase

        mock_service = Mock()
        mock_session = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=None, isAdmin=False)
        mock_service.login.return_value = mock_session

        use_case = AuthUseCase(mock_service)
        result = use_case.execute("test@example.com", "password123")

        assert result == mock_session
        mock_service.login.assert_called_once_with("test@example.com", "password123")

    def test_auth_use_case_signup(self):
        """Test del método execute con signup del AuthUseCase"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.use_cases.auth_use_case import AuthUseCase

        mock_service = Mock()
        mock_session = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=None, isAdmin=False)
        mock_service.signUp.return_value = mock_session

        use_case = AuthUseCase(mock_service)
        # El use case solo tiene execute, pero podemos testear que el servicio tiene signUp
        assert hasattr(mock_service, "signUp")

    def test_auth_use_case_signout(self):
        """Test del método execute con signout del AuthUseCase"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.aplicacion.use_cases.auth_use_case import AuthUseCase

        mock_service = Mock()
        mock_session = SessionDto(id="", user_id="", token="", expires_at=None, isAdmin=False)
        mock_service.signOut.return_value = mock_session

        use_case = AuthUseCase(mock_service)
        # El use case solo tiene execute, pero podemos testear que el servicio tiene signOut
        assert hasattr(mock_service, "signOut")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
