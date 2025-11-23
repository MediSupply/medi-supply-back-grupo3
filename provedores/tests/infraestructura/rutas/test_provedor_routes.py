"""
Tests unitarios para las rutas de proveedores
"""

from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from src.infraestructura.cmd.provedor_cmd import ProvedorCmd
from src.infraestructura.rutas.provedor_routes import create_provedor_routes


class TestProvedorRoutes:
    """Tests para las rutas de proveedores"""

    @pytest.fixture
    def mock_controller(self):
        """Fixture para crear un controlador mock"""
        return MagicMock(spec=ProvedorCmd)

    @pytest.fixture
    def app(self):
        """Fixture para crear una app Flask para tests"""
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    @pytest.fixture
    def routes(self, mock_controller, app):
        """Fixture para crear las rutas"""
        routes = create_provedor_routes(mock_controller)
        app.register_blueprint(routes)
        return routes

    def test_create_provedor_routes(self, mock_controller):
        """Test de creación de rutas"""
        routes = create_provedor_routes(mock_controller)
        assert routes is not None
        assert routes.name == "provedores"
        assert routes.url_prefix == "/provedores"

    def test_obtener_todos_los_provedores(self, mock_controller, app, routes):
        """Test de ruta GET /provedores"""
        mock_response = ({"success": True, "data": []}, 200)
        mock_controller.obtener_todos_los_provedores.return_value = mock_response

        with app.test_client() as client:
            response = client.get("/provedores")
            assert response.status_code == 200
            mock_controller.obtener_todos_los_provedores.assert_called_once()

    def test_obtener_provedor_por_id(self, mock_controller, app, routes):
        """Test de ruta GET /provedores/<id>"""
        mock_response = ({"success": True, "data": {"id": 1}}, 200)
        mock_controller.obtener_provedor_por_id.return_value = mock_response

        with app.test_client() as client:
            response = client.get("/provedores/1")
            assert response.status_code == 200
            mock_controller.obtener_provedor_por_id.assert_called_once_with(1)

    def test_obtener_provedor_por_nit(self, mock_controller, app, routes):
        """Test de ruta GET /provedores/nit/<nit>"""
        mock_response = ({"success": True, "data": {"nit": 900123456}}, 200)
        mock_controller.obtener_provedor_por_nit.return_value = mock_response

        with app.test_client() as client:
            response = client.get("/provedores/nit/900123456")
            assert response.status_code == 200
            mock_controller.obtener_provedor_por_nit.assert_called_once_with(900123456)

    def test_obtener_provedores_por_pais(self, mock_controller, app, routes):
        """Test de ruta GET /provedores/pais/<pais>"""
        mock_response = ({"success": True, "data": []}, 200)
        mock_controller.obtener_provedores_por_pais.return_value = mock_response

        with app.test_client() as client:
            response = client.get("/provedores/pais/colombia")
            assert response.status_code == 200
            mock_controller.obtener_provedores_por_pais.assert_called_once_with("colombia")

    def test_buscar_provedores_por_nombre(self, mock_controller, app, routes):
        """Test de ruta GET /provedores/buscar?nombre=<nombre>"""
        mock_response = ({"success": True, "data": []}, 200)
        mock_controller.buscar_provedores_por_nombre.return_value = mock_response

        with app.test_client() as client:
            response = client.get("/provedores/buscar?nombre=Tecnología")
            assert response.status_code == 200
            mock_controller.buscar_provedores_por_nombre.assert_called_once_with("Tecnología")

    def test_buscar_provedores_sin_nombre(self, mock_controller, app, routes):
        """Test de ruta GET /provedores/buscar sin parámetro nombre"""
        with app.test_client() as client:
            response = client.get("/provedores/buscar")
            assert response.status_code == 400
            mock_controller.buscar_provedores_por_nombre.assert_not_called()
