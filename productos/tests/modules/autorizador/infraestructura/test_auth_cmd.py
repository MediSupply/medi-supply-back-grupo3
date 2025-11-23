"""
Tests unitarios para AuthCmd
"""

from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from src.modules.autorizador.infraestructura.cmd.auth_cmd import AuthCmd


class TestAuthCmd:
    """Tests para AuthCmd"""

    @pytest.fixture
    def mock_auth_service(self):
        """Fixture para crear un mock del servicio de autenticación"""
        return MagicMock()

    @pytest.fixture
    def app(self):
        """Fixture para crear una app Flask para tests"""
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    def test_auth_cmd_init(self, mock_auth_service):
        """Test de inicialización de AuthCmd"""
        cmd = AuthCmd(mock_auth_service)
        assert cmd.auth_service == mock_auth_service

    def test_validate_token_success(self, mock_auth_service, app):
        """Test de validación de token exitosa"""
        mock_auth_service.validate_token.return_value = True
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(headers={"Authorization": "Bearer valid-token"}):
            response, status_code = cmd.validate_token()

        assert status_code == 200
        assert response.get_json()["valid"] is True
        mock_auth_service.validate_token.assert_called_once()

    def test_validate_token_invalid(self, mock_auth_service, app):
        """Test de validación de token inválido"""
        mock_auth_service.validate_token.return_value = False
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(headers={"Authorization": "Bearer invalid-token"}):
            response, status_code = cmd.validate_token()

        assert status_code == 401
        assert response.get_json()["valid"] is False
        mock_auth_service.validate_token.assert_called_once()

    def test_validate_token_missing(self, mock_auth_service, app):
        """Test de validación sin token"""
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context():
            response, status_code = cmd.validate_token()

        assert status_code == 401
        assert "error" in response.get_json()
        mock_auth_service.validate_token.assert_not_called()

    def test_validate_token_invalid_format(self, mock_auth_service, app):
        """Test de validación con formato inválido"""
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(headers={"Authorization": "InvalidFormat token"}):
            response, status_code = cmd.validate_token()

        assert status_code == 401
        assert "error" in response.get_json()

    def test_validate_token_error(self, mock_auth_service, app):
        """Test de validación con error"""
        mock_auth_service.validate_token.side_effect = Exception("Error de validación")
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(headers={"Authorization": "Bearer token"}):
            response, status_code = cmd.validate_token()

        assert status_code == 500
        assert "error" in response.get_json()

    def test_authorize_access_success(self, mock_auth_service, app):
        """Test de autorización de acceso exitosa"""
        mock_auth_service.authorize_access.return_value = True
        mock_auth_service.get_user_info.return_value = {"user_id": "user-001", "role": "ADMIN"}
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(
            headers={"Authorization": "Bearer valid-token"}, json={"route": "/productos", "method": "GET"}, method="POST"
        ):
            response, status_code = cmd.authorize_access()

        assert status_code == 200
        assert response.get_json()["authorized"] is True
        assert "user_info" in response.get_json()

    def test_authorize_access_denied(self, mock_auth_service, app):
        """Test de autorización denegada"""
        mock_auth_service.authorize_access.return_value = False
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(
            headers={"Authorization": "Bearer token"}, json={"route": "/productos", "method": "GET"}, method="POST"
        ):
            response, status_code = cmd.authorize_access()

        assert status_code == 403
        assert response.get_json()["authorized"] is False

    def test_authorize_access_missing_data(self, mock_auth_service, app):
        """Test de autorización sin datos"""
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(method="POST"):
            # request.get_json() puede retornar None y causar un error 500
            # Necesitamos mockear request.get_json para que retorne None
            from flask import request

            with patch.object(request, "get_json", return_value=None):
                response, status_code = cmd.authorize_access()

        assert status_code == 400
        assert "error" in response.get_json()

    def test_authorize_access_error(self, mock_auth_service, app):
        """Test de autorización con error"""
        mock_auth_service.authorize_access.side_effect = Exception("Error de autorización")
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(
            headers={"Authorization": "Bearer token"}, json={"route": "/productos", "method": "GET"}, method="POST"
        ):
            response, status_code = cmd.authorize_access()

        assert status_code == 500
        assert "error" in response.get_json()

    def test_get_user_info_success(self, mock_auth_service, app):
        """Test de obtener información de usuario exitosa"""
        mock_user_info = {"user_id": "user-001", "role": "ADMIN", "permissions": {}}
        mock_auth_service.get_user_info.return_value = mock_user_info
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(headers={"Authorization": "Bearer valid-token"}):
            response, status_code = cmd.get_user_info()

        assert status_code == 200
        assert "user_info" in response.get_json()
        mock_auth_service.get_user_info.assert_called_once()

    def test_get_user_info_invalid_token(self, mock_auth_service, app):
        """Test de obtener información con token inválido"""
        mock_auth_service.get_user_info.return_value = None
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(headers={"Authorization": "Bearer invalid-token"}):
            response, status_code = cmd.get_user_info()

        assert status_code == 401
        assert "error" in response.get_json()

    def test_get_user_info_missing_token(self, mock_auth_service, app):
        """Test de obtener información sin token"""
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context():
            response, status_code = cmd.get_user_info()

        assert status_code == 401
        assert "error" in response.get_json()

    def test_get_user_info_error(self, mock_auth_service, app):
        """Test de obtener información con error"""
        mock_auth_service.get_user_info.side_effect = Exception("Error al obtener información")
        cmd = AuthCmd(mock_auth_service)

        with app.test_request_context(headers={"Authorization": "Bearer token"}):
            response, status_code = cmd.get_user_info()

        assert status_code == 500
        assert "error" in response.get_json()
