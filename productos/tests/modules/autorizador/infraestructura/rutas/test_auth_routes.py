"""
Tests unitarios para las rutas de autorización
"""

from unittest.mock import MagicMock

import pytest
from flask import Flask
from src.modules.autorizador.infraestructura.rutas.auth_routes import create_auth_routes


class TestAuthRoutes:
    """Tests para las rutas de autorización"""

    @pytest.fixture
    def mock_controller(self):
        """Fixture para crear un mock del controlador"""
        return MagicMock()

    @pytest.fixture
    def auth_routes(self, mock_controller):
        """Fixture para crear las rutas de autorización"""
        return create_auth_routes(mock_controller)

    @pytest.fixture
    def app(self):
        """Fixture para crear una app Flask para tests"""
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    @pytest.fixture
    def client(self, app, auth_routes):
        """Fixture para crear un cliente de pruebas Flask"""
        app.register_blueprint(auth_routes)
        return app.test_client()

    def test_create_auth_routes(self, mock_controller):
        """Test de creación de rutas"""
        routes = create_auth_routes(mock_controller)

        assert routes is not None
        assert routes.name == "auth"
        assert routes.url_prefix == "/auth"

    def test_route_validate_token(self, client, mock_controller):
        """Test de ruta POST /auth/validate"""
        mock_controller.validate_token.return_value = ({"valid": True, "message": "Token válido"}, 200)

        response = client.post("/auth/validate", headers={"Authorization": "Bearer token"})

        assert response.status_code == 200
        mock_controller.validate_token.assert_called_once()

    def test_route_authorize_access(self, client, mock_controller):
        """Test de ruta POST /auth/authorize"""
        mock_controller.authorize_access.return_value = (
            {"authorized": True, "message": "Acceso autorizado"},
            200,
        )

        response = client.post(
            "/auth/authorize",
            json={"route": "/productos", "method": "GET"},
            headers={"Authorization": "Bearer token"},
        )

        assert response.status_code == 200
        mock_controller.authorize_access.assert_called_once()

    def test_route_get_user_info(self, client, mock_controller):
        """Test de ruta POST /auth/user-info"""
        mock_controller.get_user_info.return_value = (
            {"user_info": {"user_id": "user-001", "role": "ADMIN"}},
            200,
        )

        response = client.post("/auth/user-info", headers={"Authorization": "Bearer token"})

        assert response.status_code == 200
        mock_controller.get_user_info.assert_called_once()

    def test_route_get_resources(self, client, mock_controller):
        """Test de ruta GET /auth/resources"""
        response = client.get("/auth/resources")

        assert response.status_code == 200
        data = response.get_json()
        assert data["microservice"] == "productos"
        assert "resources" in data
        assert "actions" in data
        assert "endpoints" in data
        # El controlador no debe ser llamado para esta ruta
        mock_controller.validate_token.assert_not_called()
        mock_controller.authorize_access.assert_not_called()
        mock_controller.get_user_info.assert_not_called()
