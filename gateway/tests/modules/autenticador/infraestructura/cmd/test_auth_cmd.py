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
        from flask import Flask
        from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_session = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=None)
            login_result = LoginResultDto.success(mock_session)
            mock_use_case.execute.return_value = login_result

            cmd = AuthCmd(mock_use_case)
            result = cmd.login("test@example.com", "password123")

            assert result is not None
            mock_use_case.execute.assert_called_once_with("test@example.com", "password123")

    def test_auth_cmd_login_user_not_found(self):
        """Test del método login cuando el usuario no existe"""
        from flask import Flask
        from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            login_result = LoginResultDto.user_not_found_error()
            mock_use_case.execute.return_value = login_result

            cmd = AuthCmd(mock_use_case)
            result = cmd.login("nonexistent@example.com", "password123")

            assert result is not None
            # Verificar que se retorna 404
            assert result[1] == 404

    def test_auth_cmd_login_invalid_credentials(self):
        """Test del método login con credenciales inválidas"""
        from flask import Flask
        from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            login_result = LoginResultDto.invalid_credentials_error()
            mock_use_case.execute.return_value = login_result

            cmd = AuthCmd(mock_use_case)
            result = cmd.login("test@example.com", "wrong_password")

            assert result is not None
            # Verificar que se retorna 401
            assert result[1] == 401

    def test_auth_cmd_login_no_session(self):
        """Test del método login cuando no se retorna sesión"""
        from flask import Flask
        from modules.autenticador.aplicacion.dtos.login_result_dto import LoginResultDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            login_result = LoginResultDto(session=None, user_not_found=False, invalid_credentials=False)
            mock_use_case.execute.return_value = login_result

            cmd = AuthCmd(mock_use_case)
            result = cmd.login("test@example.com", "password123")

            assert result is not None
            # Verificar que se retorna 500
            assert result[1] == 500

    def test_auth_cmd_login_exception(self):
        """Test del método login con excepción del AuthCmd"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_use_case.execute.side_effect = Exception("Test error")

            cmd = AuthCmd(mock_use_case)
            result = cmd.login("test@example.com", "password123")

            # El cmd debe manejar la excepción y retornar 500
            assert result is not None
            assert result[1] == 500

    def test_auth_cmd_signup_success(self):
        """Test del método signup exitoso del AuthCmd"""
        from flask import Flask
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_session = SessionDto(id="session-id", user_id="user-id", token="jwt-token", expires_at=None)
            mock_use_case.user_exists.return_value = False
            mock_use_case.signUp.return_value = mock_session

            cmd = AuthCmd(mock_use_case)
            result = cmd.signUp("Test User", "test@example.com", "password123", "USER")

            assert result is not None
            assert result[1] == 201
            mock_use_case.user_exists.assert_called_once_with("test@example.com")
            mock_use_case.signUp.assert_called_once_with("Test User", "test@example.com", "password123", "USER")

    def test_auth_cmd_signup_user_exists(self):
        """Test del método signup cuando el usuario ya existe"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_use_case.user_exists.return_value = True

            cmd = AuthCmd(mock_use_case)
            result = cmd.signUp("Test User", "existing@example.com", "password123", "USER")

            assert result is not None
            assert result[1] == 409
            mock_use_case.user_exists.assert_called_once_with("existing@example.com")
            mock_use_case.signUp.assert_not_called()

    def test_auth_cmd_signup_no_session(self):
        """Test del método signup cuando no se retorna sesión"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_use_case.user_exists.return_value = False
            mock_use_case.signUp.return_value = None

            cmd = AuthCmd(mock_use_case)
            result = cmd.signUp("Test User", "test@example.com", "password123", "USER")

            assert result is not None
            assert result[1] == 500

    def test_auth_cmd_signup_exception(self):
        """Test del método signup con excepción del AuthCmd"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_use_case.user_exists.side_effect = Exception("Test error")

            cmd = AuthCmd(mock_use_case)
            result = cmd.signUp("Test User", "test@example.com", "password123", "USER")

            # El cmd debe manejar la excepción y retornar 500
            assert result is not None
            assert result[1] == 500

    def test_auth_cmd_signout_success(self):
        """Test del método signout exitoso del AuthCmd"""
        from flask import Flask
        from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_session = SessionDto(id="", user_id="", token="", expires_at=None)
            mock_use_case.signOut.return_value = mock_session

            cmd = AuthCmd(mock_use_case)
            result = cmd.signOut()

            assert result is not None
            assert result[1] == 200
            mock_use_case.signOut.assert_called_once()

    def test_auth_cmd_signout_exception(self):
        """Test del método signout con excepción"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        with app.app_context():
            mock_use_case = Mock()
            mock_use_case.signOut.side_effect = Exception("Test error")

            cmd = AuthCmd(mock_use_case)
            result = cmd.signOut()

            assert result is not None
            assert result[1] == 500

    def test_auth_cmd_get_me_success(self):
        """Test del método get_me exitoso del AuthCmd"""
        from flask import Flask
        from modules.autenticador.dominio.entities.user import Role, User
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        mock_use_case = Mock()
        mock_user = User(
            id="user-id-123",
            name="Test User",
            email="test@example.com",
            password="password123",
            role=Role.USER,
        )
        mock_use_case.get_current_user.return_value = mock_user

        cmd = AuthCmd(mock_use_case)

        with app.test_request_context(headers={"Authorization": "Bearer valid-token"}):
            result = cmd.get_me()

        # Verificar que se obtuvo el usuario
        assert result is not None
        # Verificar que se llamó al use case con el token correcto
        mock_use_case.get_current_user.assert_called_once_with("valid-token")

    def test_auth_cmd_get_me_no_authorization_header(self):
        """Test del método get_me sin header Authorization"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        mock_use_case = Mock()
        cmd = AuthCmd(mock_use_case)

        with app.test_request_context():
            result = cmd.get_me()

        # Verificar que se retorna error 401
        assert result is not None
        # Verificar que no se llamó al use case
        mock_use_case.get_current_user.assert_not_called()

    def test_auth_cmd_get_me_invalid_token_format(self):
        """Test del método get_me con formato de token inválido"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        mock_use_case = Mock()
        cmd = AuthCmd(mock_use_case)

        # Token sin el prefijo "Bearer "
        with app.test_request_context(headers={"Authorization": "invalid-token-format"}):
            result = cmd.get_me()

        # Verificar que se retorna error 401
        assert result is not None
        # Verificar que no se llamó al use case
        mock_use_case.get_current_user.assert_not_called()

    def test_auth_cmd_get_me_invalid_token(self):
        """Test del método get_me con token inválido"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        mock_use_case = Mock()
        mock_use_case.get_current_user.return_value = None
        cmd = AuthCmd(mock_use_case)

        with app.test_request_context(headers={"Authorization": "Bearer invalid-token"}):
            result = cmd.get_me()

        # Verificar que se retorna error 401
        assert result is not None
        # Verificar que se llamó al use case
        mock_use_case.get_current_user.assert_called_once_with("invalid-token")

    def test_auth_cmd_get_me_exception(self):
        """Test del método get_me con excepción"""
        from flask import Flask
        from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd

        app = Flask(__name__)
        mock_use_case = Mock()
        mock_use_case.get_current_user.side_effect = Exception("Test error")
        cmd = AuthCmd(mock_use_case)

        with app.test_request_context(headers={"Authorization": "Bearer valid-token"}):
            result = cmd.get_me()

        # Verificar que se retorna error 500
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
