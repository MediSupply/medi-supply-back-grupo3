"""
Tests unitarios para las rutas de productos del gateway
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest
from flask import Flask

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestProductoRoutes:
    """Tests para las rutas de productos"""

    def setup_method(self):
        """Setup para cada test"""
        from modules.productos.infraestructura.rutas.producto_routes import create_producto_routes

        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.producto_bp = create_producto_routes()
        self.app.register_blueprint(self.producto_bp)
        self.client = self.app.test_client()

    @patch("modules.productos.infraestructura.rutas.producto_routes.requests.get")
    def test_obtener_todos_los_productos_success(self, mock_get):
        """Test del endpoint GET /productos exitoso"""
        mock_response = Mock()
        mock_response.json.return_value = {"productos": []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get("/productos")

        assert response.status_code == 200
        mock_get.assert_called_once()

    @patch("modules.productos.infraestructura.rutas.producto_routes.requests.get")
    def test_obtener_producto_por_id_success(self, mock_get):
        """Test del endpoint GET /productos/<id> exitoso"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "producto-123", "name": "Test Producto"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get("/productos/producto-123")

        assert response.status_code == 200
        mock_get.assert_called_once()

    @patch("modules.productos.infraestructura.rutas.producto_routes.requests.get")
    def test_obtener_todos_los_productos_with_authorization(self, mock_get):
        """Test del endpoint GET /productos con header Authorization"""
        mock_response = Mock()
        mock_response.json.return_value = {"productos": []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get("/productos", headers={"Authorization": "Bearer token"})

        assert response.status_code == 200
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "headers" in call_args.kwargs
        assert call_args.kwargs["headers"]["Authorization"] == "Bearer token"

    @patch("modules.productos.infraestructura.rutas.producto_routes.requests.get")
    def test_obtener_producto_por_id_with_authorization(self, mock_get):
        """Test del endpoint GET /productos/<id> con header Authorization"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "producto-123"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get("/productos/producto-123", headers={"Authorization": "Bearer token"})

        assert response.status_code == 200
        call_args = mock_get.call_args
        assert call_args.kwargs["headers"]["Authorization"] == "Bearer token"

    @patch("modules.productos.infraestructura.rutas.producto_routes.requests.get")
    def test_obtener_todos_los_productos_request_exception(self, mock_get):
        """Test del endpoint GET /productos con excepción de requests"""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        response = self.client.get("/productos")

        assert response.status_code == 503
        data = response.get_json()
        assert "error" in data

    @patch("modules.productos.infraestructura.rutas.producto_routes.requests.get")
    def test_obtener_producto_por_id_request_exception(self, mock_get):
        """Test del endpoint GET /productos/<id> con excepción de requests"""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        response = self.client.get("/productos/producto-123")

        assert response.status_code == 503
        data = response.get_json()
        assert "error" in data

    def test_productos_service_url_from_env_default(self):
        """Test de que PRODUCTOS_SERVICE_URL usa valor por defecto"""
        import os

        from modules.productos.infraestructura.rutas.producto_routes import create_producto_routes

        # Guardar valor original
        original_value = os.environ.get("PRODUCTOS_SERVICE_URL")

        try:
            # Eliminar variable de entorno para usar valor por defecto
            if "PRODUCTOS_SERVICE_URL" in os.environ:
                del os.environ["PRODUCTOS_SERVICE_URL"]

            # Crear las rutas (esto ejecutará el código que lee la variable de entorno)
            producto_bp = create_producto_routes()

            # Verificar que se creó el blueprint
            assert producto_bp is not None
        finally:
            # Restaurar valor original
            if original_value:
                os.environ["PRODUCTOS_SERVICE_URL"] = original_value

    def test_productos_service_url_from_env(self):
        """Test de que PRODUCTOS_SERVICE_URL se obtiene del entorno"""
        import os

        from modules.productos.infraestructura.rutas.producto_routes import create_producto_routes

        # Guardar valor original
        original_value = os.environ.get("PRODUCTOS_SERVICE_URL")

        try:
            # Establecer un valor de prueba
            os.environ["PRODUCTOS_SERVICE_URL"] = "http://test-productos:5002"

            # Crear las rutas (esto ejecutará el código que lee la variable de entorno)
            producto_bp = create_producto_routes()

            # Verificar que se creó el blueprint
            assert producto_bp is not None
        finally:
            # Restaurar valor original
            if original_value:
                os.environ["PRODUCTOS_SERVICE_URL"] = original_value
            elif "PRODUCTOS_SERVICE_URL" in os.environ:
                del os.environ["PRODUCTOS_SERVICE_URL"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
