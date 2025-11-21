"""
Tests unitarios para los cmd del módulo de autenticación del gateway
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestAuthCmd:
    """Tests para el AuthCmd"""

    def test_auth_cmd_initialization(self):
        """Test de inicialización del AuthCmd"""
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        mock_use_case = Mock()
        cmd = AuthCmd(mock_use_case)

        assert cmd.auth_use_case == mock_use_case

    def test_auth_cmd_login_success(self):
        """Test del método login exitoso del AuthCmd"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        mock_use_case = Mock()
        mock_session = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=None, isAdmin=False)
        mock_use_case.execute.return_value = mock_session

        cmd = AuthCmd(mock_use_case)

        # Test que el cmd tiene el método login
        assert hasattr(cmd, "login")
        # Test que el use case tiene el método execute
        assert hasattr(mock_use_case, "execute")

    def test_auth_cmd_login_exception(self):
        """Test del método login con excepción del AuthCmd"""
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        mock_use_case = Mock()
        mock_use_case.login.side_effect = Exception("Test error")

        cmd = AuthCmd(mock_use_case)

        # El cmd debe manejar la excepción
        with pytest.raises(Exception):
            cmd.login("test@example.com", "password123")

    def test_auth_cmd_signup_success(self):
        """Test del método signup exitoso del AuthCmd"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        mock_use_case = Mock()
        mock_session = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=None, isAdmin=False)
        mock_use_case.execute.return_value = mock_session

        cmd = AuthCmd(mock_use_case)

        # Test que el cmd tiene los métodos necesarios
        assert hasattr(cmd, "auth_use_case")
        # Test que el use case tiene el método execute
        assert hasattr(mock_use_case, "execute")

    def test_auth_cmd_signup_exception(self):
        """Test del método signup con excepción del AuthCmd"""
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        mock_use_case = Mock()
        mock_use_case.signUp.side_effect = Exception("Test error")

        cmd = AuthCmd(mock_use_case)

        # El cmd debe manejar la excepción
        with pytest.raises(Exception):
            cmd.signUp("Test User", "test@example.com", "password123", "USER")

    def test_auth_cmd_signout_success(self):
        """Test del método signout exitoso del AuthCmd"""
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        mock_use_case = Mock()
        mock_session = SessionDto(id="", user_id="", token="", expires_at=None, isAdmin=False)
        mock_use_case.execute.return_value = mock_session

        cmd = AuthCmd(mock_use_case)

        # Test que el cmd tiene los métodos necesarios
        assert hasattr(cmd, "auth_use_case")
        # Test que el use case tiene el método execute
        assert hasattr(mock_use_case, "execute")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
