"""
Tests unitarios para las rutas de productos
"""

from unittest.mock import MagicMock
import pytest
from flask import Flask

from src.infraestructura.rutas.producto_routes import create_producto_routes


class TestProductoRoutes:
    """Tests para las rutas de productos"""

    @pytest.fixture
    def mock_controller(self):
        """Fixture para crear un mock del controlador"""
        return MagicMock()

    @pytest.fixture
    def producto_routes(self, mock_controller):
        """Fixture para crear las rutas de productos"""
        return create_producto_routes(mock_controller)

    @pytest.fixture
    def app(self):
        """Fixture para crear una app Flask para tests"""
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    @pytest.fixture
    def client(self, app, producto_routes):
        """Fixture para crear un cliente de pruebas Flask"""
        app.register_blueprint(producto_routes)
        return app.test_client()

    def test_create_producto_routes(self, mock_controller):
        """Test de creación de rutas"""
        routes = create_producto_routes(mock_controller)

        assert routes is not None
        assert routes.name == "productos"
        assert routes.url_prefix == "/productos"

    def test_route_obtener_todos_los_productos(self, client, mock_controller):
        """Test de ruta GET /productos"""
        mock_controller.obtener_todos_los_productos.return_value = (
            {"id": "prod-001", "nombre": "Producto 1"},
            200,
        )

        response = client.get("/productos")

        assert response.status_code == 200
        mock_controller.obtener_todos_los_productos.assert_called_once()

    def test_route_obtener_producto_por_id(self, client, mock_controller):
        """Test de ruta GET /productos/<id>"""
        mock_controller.obtener_producto_por_id.return_value = (
            {"id": "prod-001", "nombre": "Producto 1"},
            200,
        )

        response = client.get("/productos/prod-001")

        assert response.status_code == 200
        mock_controller.obtener_producto_por_id.assert_called_once_with("prod-001")

    def test_route_obtener_productos_por_categoria(self, client, mock_controller):
        """Test de ruta GET /productos/categoria/<categoria>"""
        mock_controller.obtener_productos_por_categoria.return_value = (
            [{"id": "prod-001", "nombre": "Producto 1", "categoria": "electronicos"}],
            200,
        )

        response = client.get("/productos/categoria/electronicos")

        assert response.status_code == 200
        mock_controller.obtener_productos_por_categoria.assert_called_once_with("electronicos")

    def test_route_buscar_productos_por_nombre(self, client, mock_controller):
        """Test de ruta GET /productos/buscar?nombre=..."""
        mock_controller.buscar_productos_por_nombre.return_value = (
            [{"id": "prod-001", "nombre": "Laptop Gaming"}],
            200,
        )

        response = client.get("/productos/buscar?nombre=Laptop")

        assert response.status_code == 200
        mock_controller.buscar_productos_por_nombre.assert_called_once_with("Laptop")

    def test_route_buscar_productos_sin_nombre(self, client, mock_controller):
        """Test de ruta GET /productos/buscar sin parámetro nombre"""
        response = client.get("/productos/buscar")

        assert response.status_code == 400
        assert "error" in response.get_json()
        assert "nombre" in response.get_json()["error"].lower() or "requerido" in response.get_json()["error"].lower()
        # El controlador no debe ser llamado si falta el parámetro
        mock_controller.buscar_productos_por_nombre.assert_not_called()

    def test_route_buscar_productos_con_nombre_vacio(self, client, mock_controller):
        """Test de ruta GET /productos/buscar con parámetro nombre vacío"""
        response = client.get("/productos/buscar?nombre=")

        assert response.status_code == 400
        assert "error" in response.get_json()
        mock_controller.buscar_productos_por_nombre.assert_not_called()

    def test_route_obtener_producto_por_id_diferentes_ids(self, client, mock_controller):
        """Test de ruta GET /productos/<id> con diferentes IDs"""
        mock_controller.obtener_producto_por_id.return_value = (
            {"id": "prod-999", "nombre": "Producto Test"},
            200,
        )

        response = client.get("/productos/prod-999")

        assert response.status_code == 200
        mock_controller.obtener_producto_por_id.assert_called_once_with("prod-999")

    def test_route_obtener_productos_por_categoria_diferentes_categorias(self, client, mock_controller):
        """Test de ruta GET /productos/categoria/<categoria> con diferentes categorías"""
        mock_controller.obtener_productos_por_categoria.return_value = (
            [{"id": "prod-002", "nombre": "Producto 2", "categoria": "deportes"}],
            200,
        )

        response = client.get("/productos/categoria/deportes")

        assert response.status_code == 200
        mock_controller.obtener_productos_por_categoria.assert_called_once_with("deportes")

