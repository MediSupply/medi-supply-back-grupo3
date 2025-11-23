"""
Tests unitarios para AuthorizationService
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import jwt
import pytest
from src.modules.autorizador.aplicacion.servicios.authorization_service import AuthorizationService
from src.modules.autorizador.dominio.entities.token_payload import Role, TokenPayload
from src.modules.autorizador.dominio.exceptions import (
    ExpiredTokenError,
    InsufficientPermissionsError,
    InvalidTokenError,
    MissingTokenError,
)


class TestAuthorizationService:
    """Tests para AuthorizationService"""

    @pytest.fixture
    def secret_key(self):
        """Fixture para la clave secreta"""
        return "test-secret-key-with-at-least-32-characters-for-security"

    @pytest.fixture
    def auth_service(self, secret_key):
        """Fixture para crear un AuthorizationService"""
        return AuthorizationService(secret_key, "HS256")

    def test_authorization_service_init(self, secret_key):
        """Test de inicialización de AuthorizationService"""
        service = AuthorizationService(secret_key, "HS256")
        assert service.token_validator is not None
        assert service.access_validator is not None

    def test_validate_token_valid(self, auth_service, secret_key):
        """Test de validación de token válido"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        token_payload = auth_service.validate_token(header)
        assert token_payload is not None
        assert token_payload.user_id == "user-001"
        assert token_payload.role == Role.ADMIN

    def test_validate_token_missing(self, auth_service):
        """Test de validación de token faltante"""
        with pytest.raises(MissingTokenError):
            auth_service.validate_token(None)

    def test_validate_token_invalid(self, auth_service):
        """Test de validación de token inválido"""
        with pytest.raises(InvalidTokenError):
            auth_service.validate_token("Bearer invalid.token")

    def test_validate_access_valid(self, auth_service, secret_key):
        """Test de validación de acceso válido"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        token_payload = auth_service.validate_token(header)
        result = auth_service.validate_access(token_payload, "/provedores", "GET")
        assert result is True

    def test_validate_access_insufficient_permissions(self, auth_service, secret_key):
        """Test de validación de acceso con permisos insuficientes"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "USER",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        token_payload = auth_service.validate_token(header)
        with pytest.raises(InsufficientPermissionsError):
            auth_service.validate_access(token_payload, "/provedores", "GET")

    def test_authorize_request_public_route(self, auth_service):
        """Test de autorización de request a ruta pública"""
        authorized, token_payload = auth_service.authorize_request(None, "/health", "GET")
        assert authorized is True
        assert token_payload is None

    def test_authorize_request_valid(self, auth_service, secret_key):
        """Test de autorización de request válida"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        authorized, token_payload = auth_service.authorize_request(header, "/provedores", "GET")
        assert authorized is True
        assert token_payload is not None

    def test_authorize_request_denied(self, auth_service):
        """Test de autorización de request denegada"""
        authorized, token_payload = auth_service.authorize_request(None, "/provedores", "GET")
        assert authorized is False
        assert token_payload is None

    def test_authorize_request_insufficient_permissions(self, auth_service, secret_key):
        """Test de autorización de request con permisos insuficientes"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "USER",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        authorized, token_payload = auth_service.authorize_request(header, "/provedores", "POST")
        assert authorized is False
        assert token_payload is None

    def test_is_public_route(self, auth_service):
        """Test de verificación de ruta pública"""
        assert auth_service.is_public_route("/health") is True
        assert auth_service.is_public_route("/auth/validate") is True
        assert auth_service.is_public_route("/provedores") is False

    def test_get_user_info_valid(self, auth_service, secret_key):
        """Test de obtención de información de usuario válido"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        user_info = auth_service.get_user_info(header)
        assert user_info is not None
        assert user_info["role"] == "ADMIN"
        assert user_info["user_id"] == "user-001"

    def test_get_user_info_invalid(self, auth_service):
        """Test de obtención de información de usuario inválido"""
        user_info = auth_service.get_user_info("Bearer invalid.token")
        assert user_info is None
