"""
Tests unitarios para AccessValidator
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from src.modules.autorizador.aplicacion.use_cases.access_validator import AccessValidator
from src.modules.autorizador.dominio.entities.resource import ActionType, ResourceType
from src.modules.autorizador.dominio.entities.token_payload import Role, TokenPayload
from src.modules.autorizador.dominio.exceptions import InsufficientPermissionsError


class TestAccessValidator:
    """Tests para AccessValidator"""

    @pytest.fixture
    def validator(self):
        """Fixture para crear un AccessValidator"""
        return AccessValidator()

    @pytest.fixture
    def admin_payload(self):
        """Fixture para crear un token payload de admin"""
        return TokenPayload(
            user_id="user-001",
            role=Role.ADMIN,
            exp=datetime.utcnow() + timedelta(hours=1),
        )

    @pytest.fixture
    def user_payload(self):
        """Fixture para crear un token payload de user"""
        return TokenPayload(
            user_id="user-002",
            role=Role.USER,
            exp=datetime.utcnow() + timedelta(hours=1),
        )

    @pytest.fixture
    def viewer_payload(self):
        """Fixture para crear un token payload de viewer"""
        return TokenPayload(
            user_id="user-003",
            role=Role.VIEWER,
            exp=datetime.utcnow() + timedelta(hours=1),
        )

    def test_access_validator_init(self, validator):
        """Test de inicialización de AccessValidator"""
        assert validator is not None
        assert hasattr(validator, "route_permissions")
        assert hasattr(validator, "public_routes")

    def test_is_public_route_exact_match(self, validator):
        """Test de verificación de ruta pública (coincidencia exacta)"""
        assert validator._is_public_route("/") is True
        assert validator._is_public_route("/health") is True
        assert validator._is_public_route("/auth/resources") is True

    def test_is_public_route_prefix_match(self, validator):
        """Test de verificación de ruta pública (coincidencia por prefijo)"""
        assert validator._is_public_route("/health/check") is True
        assert validator._is_public_route("/auth/validate") is True
        assert validator._is_public_route("/auth/authorize") is True

    def test_is_public_route_private(self, validator):
        """Test de verificación de ruta privada"""
        assert validator._is_public_route("/productos") is False
        assert validator._is_public_route("/productos/123") is False

    def test_is_internal_request_with_headers(self, validator):
        """Test de verificación de petición interna con headers"""
        mock_request = MagicMock()
        mock_request.headers.get.side_effect = lambda key: {
            "X-Internal-Request": "true",
            "X-Gateway-Token": "gateway-token",
        }.get(key)

        assert validator._is_internal_request(mock_request) is True

    def test_is_internal_request_without_headers(self, validator):
        """Test de verificación de petición interna sin headers"""
        mock_request = MagicMock()
        mock_request.headers.get.return_value = None

        assert validator._is_internal_request(mock_request) is False

    def test_is_internal_request_partial_headers(self, validator):
        """Test de verificación de petición interna con headers parciales"""
        mock_request = MagicMock()
        mock_request.headers.get.side_effect = lambda key: {"X-Internal-Request": "true"}.get(key)

        assert validator._is_internal_request(mock_request) is False

    def test_validate_access_public_route(self, validator, user_payload):
        """Test de validación de acceso a ruta pública"""
        result = validator.validate_access(user_payload, "/health", "GET")
        assert result is True

    def test_validate_access_admin_read(self, validator, admin_payload):
        """Test de validación de acceso de admin para lectura"""
        result = validator.validate_access(admin_payload, "/productos", "GET")
        assert result is True

    def test_validate_access_admin_create(self, validator, admin_payload):
        """Test de validación de acceso de admin para creación"""
        result = validator.validate_access(admin_payload, "/productos", "POST")
        assert result is True

    def test_validate_access_user_read(self, validator, user_payload):
        """Test de validación de acceso de user para lectura"""
        result = validator.validate_access(user_payload, "/productos", "GET")
        assert result is True

    def test_validate_access_viewer_read(self, validator, viewer_payload):
        """Test de validación de acceso de viewer para lectura"""
        result = validator.validate_access(viewer_payload, "/productos", "GET")
        assert result is True

    def test_validate_access_viewer_create_denied(self, validator, viewer_payload):
        """Test de validación de acceso de viewer para creación (denegado)"""
        with pytest.raises(InsufficientPermissionsError):
            validator.validate_access(viewer_payload, "/productos", "POST")

    def test_validate_access_unauthorized_route(self, validator, admin_payload):
        """Test de validación de acceso a ruta no autorizada"""
        with pytest.raises(InsufficientPermissionsError):
            validator.validate_access(admin_payload, "/unauthorized-route", "GET")

    def test_get_required_permission_exact_route(self, validator):
        """Test de obtención de permiso requerido (ruta exacta)"""
        resource, action = validator._get_required_permission("/productos", "GET")
        assert resource == ResourceType.PRODUCTS
        assert action == ActionType.READ

    def test_get_required_permission_prefix_route(self, validator):
        """Test de obtención de permiso requerido (ruta con prefijo)"""
        resource, action = validator._get_required_permission("/productos/123", "GET")
        assert resource == ResourceType.PRODUCTS
        assert action == ActionType.READ

    def test_get_required_permission_unauthorized_route(self, validator):
        """Test de obtención de permiso requerido (ruta no autorizada)"""
        with pytest.raises(InsufficientPermissionsError):
            validator._get_required_permission("/unauthorized", "GET")

    def test_get_user_permissions_admin(self, validator, admin_payload):
        """Test de obtención de permisos de usuario admin"""
        permissions = validator.get_user_permissions(admin_payload)

        assert permissions["role"] == "admin"
        assert "permissions" in permissions
        assert "user_id" in permissions
        assert permissions["user_id"] == "user-001"

    def test_get_user_permissions_user(self, validator, user_payload):
        """Test de obtención de permisos de usuario user"""
        permissions = validator.get_user_permissions(user_payload)

        assert permissions["role"] == "user"
        assert "permissions" in permissions
        assert permissions["user_id"] == "user-002"

    def test_get_user_permissions_viewer(self, validator, viewer_payload):
        """Test de obtención de permisos de usuario viewer"""
        permissions = validator.get_user_permissions(viewer_payload)

        assert permissions["role"] == "viewer"
        assert "permissions" in permissions
        assert permissions["user_id"] == "user-003"
