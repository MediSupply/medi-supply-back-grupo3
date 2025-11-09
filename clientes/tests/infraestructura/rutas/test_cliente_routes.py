"""
Tests unitarios para las rutas de clientes
"""

import os
import sys
from unittest.mock import MagicMock

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteRoutes:
    """Tests para las rutas de clientes"""

    @pytest.fixture
    def mock_controller(self):
        """Fixture para crear un mock del controlador"""
        return MagicMock()

    @pytest.fixture
    def cliente_routes(self, mock_controller):
        """Fixture para crear las rutas de clientes"""
        from src.infraestructura.rutas.cliente_routes import create_cliente_routes

        return create_cliente_routes(mock_controller)

    @pytest.fixture
    def app(self):
        """Fixture para crear una app Flask para tests"""
        from flask import Flask

        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    @pytest.fixture
    def client(self, app, cliente_routes):
        """Fixture para crear un cliente de pruebas Flask"""
        app.register_blueprint(cliente_routes)
        return app.test_client()

    def test_create_cliente_routes(self, mock_controller):
        """Test de creación de rutas"""
        from src.infraestructura.rutas.cliente_routes import create_cliente_routes

        routes = create_cliente_routes(mock_controller)

        assert routes is not None
        assert routes.name == "clientes"
        assert routes.url_prefix == "/clientes"

    def test_route_obtener_todos_los_clientes(self, client, mock_controller):
        """Test de ruta GET /clientes"""
        mock_controller.obtener_todos_los_clientes.return_value = ({"success": True, "data": [], "total": 0}, 200)

        response = client.get("/clientes")

        assert response.status_code == 200
        mock_controller.obtener_todos_los_clientes.assert_called_once()

    def test_route_obtener_cliente_por_id(self, client, mock_controller):
        """Test de ruta GET /clientes/<id>"""
        mock_controller.obtener_cliente_por_id.return_value = (
            {"success": True, "data": {"id": "cli-001", "nombre": "Test"}},
            200,
        )

        response = client.get("/clientes/cli-001")

        assert response.status_code == 200
        mock_controller.obtener_cliente_por_id.assert_called_once_with("cli-001")

    def test_route_obtener_clientes_por_categoria(self, client, mock_controller):
        """Test de ruta GET /clientes/categoria/<categoria>"""
        mock_controller.obtener_clientes_por_categoria.return_value = (
            {"success": True, "data": [], "total": 0, "categoria": "hospitales"},
            200,
        )

        response = client.get("/clientes/categoria/hospitales")

        assert response.status_code == 200
        mock_controller.obtener_clientes_por_categoria.assert_called_once_with("hospitales")

    def test_route_buscar_clientes_por_nombre(self, client, mock_controller):
        """Test de ruta GET /clientes/buscar?nombre=..."""
        mock_controller.buscar_clientes_por_nombre.return_value = (
            {"success": True, "data": [], "total": 0, "busqueda": "Hospital"},
            200,
        )

        response = client.get("/clientes/buscar?nombre=Hospital")

        assert response.status_code == 200
        mock_controller.buscar_clientes_por_nombre.assert_called_once_with("Hospital")

    def test_route_buscar_clientes_sin_nombre(self, client, mock_controller):
        """Test de ruta GET /clientes/buscar sin parámetro nombre"""
        response = client.get("/clientes/buscar")

        assert response.status_code == 400
        assert "error" in response.json
        assert "nombre" in response.json["error"].lower()

    def test_route_crear_cliente(self, client, mock_controller):
        """Test de ruta POST /clientes"""
        mock_controller.crear_cliente.return_value = (
            {"success": True, "data": {"id": "cli-001", "nombre": "Test"}},
            201,
        )

        cliente_data = {
            "nombre": "Hospital Test",
            "email": "test@test.com",
            "telefono": "+57 1 111 2222",
            "direccion": "Dirección Test",
            "razon_social": "Razón Social Test",
            "nit": "900111222-3",
        }

        response = client.post("/clientes", json=cliente_data)

        assert response.status_code == 201
        mock_controller.crear_cliente.assert_called_once()
        # Verificar que se pasó el JSON correctamente
        call_args = mock_controller.crear_cliente.call_args[0][0]
        assert call_args["nombre"] == "Hospital Test"

    def test_route_crear_cliente_sin_body(self, client, mock_controller):
        """Test de ruta POST /clientes sin body"""
        response = client.post("/clientes", data=None, content_type="application/json")
        assert response.status_code == 400
        if response.json:
            assert "error" in response.json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

