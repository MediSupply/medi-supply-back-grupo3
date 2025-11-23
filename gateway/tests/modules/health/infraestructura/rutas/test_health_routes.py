"""
Tests unitarios para las rutas de health del gateway
"""

import os
import sys
from unittest.mock import Mock

import pytest
from flask import Flask

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthRoutes:
    """Tests para las rutas de health"""

    def setup_method(self):
        """Setup para cada test"""
        from modules.health.infraestructura.cmd.health_cmd import HealthCmd
        from modules.health.infraestructura.rutas.health_routes import create_health_routes

        self.mock_controller = Mock()
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.health_bp = create_health_routes(self.mock_controller)
        self.app.register_blueprint(self.health_bp)
        self.client = self.app.test_client()

    def test_health_endpoint_success(self):
        """Test del endpoint GET /health/ exitoso"""
        self.mock_controller.get_health.return_value = ({"status": "healthy"}, 200)

        response = self.client.get("/health/")

        assert response.status_code == 200
        self.mock_controller.get_health.assert_called_once()
        data = response.get_json()
        assert data["status"] == "healthy"

    def test_health_endpoint_unhealthy(self):
        """Test del endpoint GET /health/ cuando está unhealthy"""
        self.mock_controller = Mock()
        from modules.health.infraestructura.cmd.health_cmd import HealthCmd
        from modules.health.infraestructura.rutas.health_routes import create_health_routes

        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.health_bp = create_health_routes(self.mock_controller)
        self.app.register_blueprint(self.health_bp)
        self.client = self.app.test_client()

        self.mock_controller.get_health.return_value = ({"status": "unhealthy"}, 503)

        response = self.client.get("/health/")

        assert response.status_code == 503
        data = response.get_json()
        assert data["status"] == "unhealthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
