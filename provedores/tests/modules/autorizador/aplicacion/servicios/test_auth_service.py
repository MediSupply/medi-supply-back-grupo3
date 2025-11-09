"""
Tests unitarios para AuthService
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock
import pytest
import jwt

from src.modules.autorizador.aplicacion.servicios.auth_service import AuthService
from src.modules.autorizador.dominio.entities.token_payload import Role, TokenPayload
from src.modules.autorizador.dominio.exceptions import InvalidTokenError


class TestAuthService:
    """Tests para AuthService"""

    @pytest.fixture
    def secret_key(self):
        """Fixture para la clave secreta"""
        return "test-secret-key-with-at-least-32-characters-for-security"

    @pytest.fixture
    def auth_service(self, secret_key):
        """Fixture para crear un AuthService"""
        return AuthService(secret_key, "HS256")

    def test_auth_service_init(self, secret_key):
        """Test de inicialización de AuthService"""
        service = AuthService(secret_key, "HS256")
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

        result = auth_service.validate_token(header)
        assert result is True

    def test_validate_token_invalid(self, auth_service):
        """Test de validación de token inválido"""
        result = auth_service.validate_token("Bearer invalid.token")
        assert result is False

    def test_validate_token_none(self, auth_service):
        """Test de validación de token None"""
        result = auth_service.validate_token(None)
        assert result is False

    def test_get_token_payload_valid(self, auth_service, secret_key):
        """Test de obtención de payload válido"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        token_payload = auth_service.get_token_payload(header)
        assert token_payload is not None
        assert token_payload.user_id == "user-001"
        assert token_payload.role == Role.ADMIN

    def test_get_token_payload_none(self, auth_service):
        """Test de obtención de payload con header None"""
        token_payload = auth_service.get_token_payload(None)
        assert token_payload is None

    def test_get_token_payload_malformed_header(self, auth_service):
        """Test de obtención de payload con header malformado"""
        with pytest.raises(InvalidTokenError):
            auth_service.get_token_payload("Bearer")

    def test_authorize_access_public_route(self, auth_service):
        """Test de autorización de acceso a ruta pública"""
        result = auth_service.authorize_access(None, "/health", "GET", None)
        assert result is True

    def test_authorize_access_internal_request(self, auth_service):
        """Test de autorización de acceso para petición interna"""
        mock_request = MagicMock()
        mock_request.headers.get.side_effect = lambda key: {
            "X-Internal-Request": "true",
            "X-Gateway-Token": "gateway-token"
        }.get(key)

        result = auth_service.authorize_access(None, "/provedores", "GET", mock_request)
        assert result is True

    def test_authorize_access_valid_token(self, auth_service, secret_key):
        """Test de autorización de acceso con token válido"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        result = auth_service.authorize_access(header, "/provedores", "GET", None)
        assert result is True

    def test_authorize_access_no_token(self, auth_service):
        """Test de autorización de acceso sin token"""
        result = auth_service.authorize_access(None, "/provedores", "GET", None)
        assert result is False

    def test_authorize_access_insufficient_permissions(self, auth_service, secret_key):
        """Test de autorización de acceso con permisos insuficientes"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "USER",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        result = auth_service.authorize_access(header, "/provedores", "GET", None)
        assert result is False

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

    def test_get_user_info_invalid(self, auth_service, secret_key):
        """Test de obtención de información de usuario inválido"""
        # Crear un token expirado (get_token_payload devuelve None para tokens expirados)
        from datetime import datetime, timedelta
        exp = datetime.utcnow() - timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow() - timedelta(hours=2),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"
        
        # get_user_info devuelve None cuando get_token_payload devuelve None
        user_info = auth_service.get_user_info(header)
        assert user_info is None

