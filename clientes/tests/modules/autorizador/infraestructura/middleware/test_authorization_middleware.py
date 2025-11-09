"""
Tests unitarios para AuthorizationMiddleware
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import pytest
from flask import Flask
import jwt

from src.modules.autorizador.infraestructura.middleware.authorization_middleware import (
    AuthorizationMiddleware,
    create_authorization_middleware,
)
from src.modules.autorizador.aplicacion.servicios.auth_service import AuthService


class TestAuthorizationMiddleware:
    """Tests para AuthorizationMiddleware"""

    @pytest.fixture
    def secret_key(self):
        """Fixture para la clave secreta"""
        return "test-secret-key-with-at-least-32-characters-for-security"

    @pytest.fixture
    def auth_service(self, secret_key):
        """Fixture para crear un AuthService"""
        return AuthService(secret_key, "HS256")

    @pytest.fixture
    def middleware(self, auth_service):
        """Fixture para crear un AuthorizationMiddleware"""
        return AuthorizationMiddleware(auth_service)

    @pytest.fixture
    def app(self):
        """Fixture para crear una app Flask para tests"""
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    def test_middleware_init(self, auth_service):
        """Test de inicialización de AuthorizationMiddleware"""
        middleware = AuthorizationMiddleware(auth_service)
        assert middleware.auth_service == auth_service

    def test_before_request_options(self, middleware, app):
        """Test de before_request para método OPTIONS (CORS)"""
        with app.test_request_context(method="OPTIONS", path="/clientes"):
            result = middleware.before_request()
            assert result is None

    def test_before_request_public_route(self, middleware, app, secret_key):
        """Test de before_request para ruta pública"""
        with app.test_request_context(method="GET", path="/health"):
            result = middleware.before_request()
            assert result is None

    def test_before_request_authorized(self, middleware, app, secret_key):
        """Test de before_request con acceso autorizado"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        header = f"Bearer {token}"

        with app.test_request_context(
            method="GET",
            path="/clientes",
            headers={"Authorization": header}
        ):
            result = middleware.before_request()
            assert result is None

    def test_before_request_unauthorized(self, middleware, app):
        """Test de before_request sin autorización"""
        with app.test_request_context(
            method="GET",
            path="/clientes",
            headers={}
        ):
            result = middleware.before_request()
            assert result is not None
            response, status_code = result
            assert status_code == 401
            assert "error" in response.get_json()

    def test_before_request_invalid_token(self, middleware, app):
        """Test de before_request con token inválido"""
        with app.test_request_context(
            method="GET",
            path="/clientes",
            headers={"Authorization": "Bearer invalid.token"}
        ):
            result = middleware.before_request()
            assert result is not None
            response, status_code = result
            assert status_code == 401

    def test_create_authorization_middleware_valid(self, app, secret_key):
        """Test de creación de middleware válido"""
        auth_service = create_authorization_middleware(app, secret_key, "HS256")
        assert auth_service is not None
        assert isinstance(auth_service, AuthService)

    def test_create_authorization_middleware_short_secret(self, app):
        """Test de creación de middleware con clave secreta corta"""
        with pytest.raises(ValueError):
            create_authorization_middleware(app, "short", "HS256")

    def test_create_authorization_middleware_empty_secret(self, app):
        """Test de creación de middleware con clave secreta vacía"""
        with pytest.raises(ValueError):
            create_authorization_middleware(app, "", "HS256")

    def test_create_authorization_middleware_none_secret(self, app):
        """Test de creación de middleware con clave secreta None"""
        with pytest.raises(ValueError):
            create_authorization_middleware(app, None, "HS256")

    def test_create_authorization_middleware_registers_before_request(self, app, secret_key):
        """Test de que el middleware se registra en Flask"""
        create_authorization_middleware(app, secret_key, "HS256")
        
        # Verificar que se registró el before_request
        assert len(app.before_request_funcs.get(None, [])) > 0

