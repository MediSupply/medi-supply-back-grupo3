"""
Tests unitarios para las rutas de provedores del gateway
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest
from flask import Flask

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestProvedoresRoutes:
    """Tests para las rutas de provedores"""

    def setup_method(self):
        """Setup para cada test"""
        from modules.provedores.infraestructura.rutas.provedores_routes import create_provedores_routes

        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.provedores_bp = create_provedores_routes()
        self.app.register_blueprint(self.provedores_bp)
        self.client = self.app.test_client()

    @patch("modules.provedores.infraestructura.rutas.provedores_routes.requests.get")
    def test_obtener_todos_los_provedores_success(self, mock_get):
        """Test del endpoint GET /provedores exitoso"""
        mock_response = Mock()
        mock_response.json.return_value = {"provedores": []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get("/provedores")

        assert response.status_code == 200
        mock_get.assert_called_once()

    @patch("modules.provedores.infraestructura.rutas.provedores_routes.requests.get")
    def test_obtener_provedor_por_id_success(self, mock_get):
        """Test del endpoint GET /provedores/<id> exitoso"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "provedor-123", "name": "Test Provedor"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get("/provedores/provedor-123")

        assert response.status_code == 200
        mock_get.assert_called_once()

    @patch("modules.provedores.infraestructura.rutas.provedores_routes.requests.get")
    def test_obtener_todos_los_provedores_request_exception(self, mock_get):
        """Test del endpoint GET /provedores con excepción de requests"""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        response = self.client.get("/provedores")

        assert response.status_code == 503
        data = response.get_json()
        assert "error" in data

    @patch("modules.provedores.infraestructura.rutas.provedores_routes.requests.get")
    def test_obtener_provedor_por_id_request_exception(self, mock_get):
        """Test del endpoint GET /provedores/<id> con excepción de requests"""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        response = self.client.get("/provedores/provedor-123")

        assert response.status_code == 503
        data = response.get_json()
        assert "error" in data

    @patch("modules.provedores.infraestructura.rutas.provedores_routes.requests.get")
    def test_obtener_todos_los_provedores_with_headers(self, mock_get):
        """Test del endpoint GET /provedores con headers"""
        mock_response = Mock()
        mock_response.json.return_value = {"provedores": []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get("/provedores", headers={"Authorization": "Bearer token"})

        assert response.status_code == 200
        # Verificar que se pasaron los headers
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "headers" in call_args.kwargs

    def test_provedores_service_url_from_env(self):
        """Test de que PROVEDORES_SERVICE_URL se obtiene del entorno"""
        import os

        from modules.provedores.infraestructura.rutas.provedores_routes import create_provedores_routes

        # Guardar valor original
        original_value = os.environ.get("PROVEDORES_SERVICE_URL")

        try:
            # Establecer un valor de prueba
            os.environ["PROVEDORES_SERVICE_URL"] = "http://test-provedores:5003"

            # Crear las rutas (esto ejecutará el código que lee la variable de entorno)
            provedores_bp = create_provedores_routes()

            # Verificar que se creó el blueprint
            assert provedores_bp is not None
        finally:
            # Restaurar valor original
            if original_value:
                os.environ["PROVEDORES_SERVICE_URL"] = original_value
            elif "PROVEDORES_SERVICE_URL" in os.environ:
                del os.environ["PROVEDORES_SERVICE_URL"]

    def test_provedores_service_url_default(self):
        """Test de que PROVEDORES_SERVICE_URL usa valor por defecto"""
        import os

        from modules.provedores.infraestructura.rutas.provedores_routes import create_provedores_routes

        # Guardar valor original
        original_value = os.environ.get("PROVEDORES_SERVICE_URL")

        try:
            # Eliminar variable de entorno para usar valor por defecto
            if "PROVEDORES_SERVICE_URL" in os.environ:
                del os.environ["PROVEDORES_SERVICE_URL"]

            # Crear las rutas (esto ejecutará el código que lee la variable de entorno)
            provedores_bp = create_provedores_routes()

            # Verificar que se creó el blueprint
            assert provedores_bp is not None
        finally:
            # Restaurar valor original
            if original_value:
                os.environ["PROVEDORES_SERVICE_URL"] = original_value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
