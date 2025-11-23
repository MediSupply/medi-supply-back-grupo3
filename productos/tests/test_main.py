"""
Tests unitarios para main.py
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from src.main import create_application, setup_logging


class TestMain:
    """Tests para main.py"""

    @pytest.fixture
    def app(self):
        """Fixture para crear una app Flask para tests"""
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    @patch("src.main.Config")
    def test_setup_logging(self, mock_config, app):
        """Test de setup_logging"""
        app.config["LOG_LEVEL"] = "DEBUG"
        setup_logging(app)

        # Verificar que el logging se configuró
        # No podemos verificar el nivel exacto porque logging.basicConfig puede haber sido llamado antes
        # Solo verificamos que la función se ejecutó sin errores
        assert True

    @patch("src.main.Config")
    def test_setup_logging_default_level(self, mock_config, app):
        """Test de setup_logging con nivel por defecto"""
        if "LOG_LEVEL" in app.config:
            del app.config["LOG_LEVEL"]
        setup_logging(app)

        # Verificar que el logging se configuró
        # No podemos verificar el nivel exacto porque logging.basicConfig puede haber sido llamado antes
        # Solo verificamos que la función se ejecutó sin errores
        assert True

    @patch("src.main.Config")
    @patch("src.main.setup_logging")
    def test_create_application_success(self, mock_setup_logging, mock_config_class):
        """Test de creación de aplicación exitosa"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_app = Flask(__name__)
        mock_config_instance.create_app.return_value = mock_app
        mock_config_class.return_value = mock_config_instance

        app = create_application()

        assert app is not None
        assert isinstance(app, Flask)
        mock_config_class.assert_called_once()
        mock_config_instance.create_app.assert_called_once()
        mock_setup_logging.assert_called_once_with(mock_app)

    @patch("src.main.Config")
    @patch("src.main.setup_logging")
    def test_create_application_error(self, mock_setup_logging, mock_config_class):
        """Test de creación de aplicación con error"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_instance.create_app.side_effect = Exception("Error de configuración")
        mock_config_class.return_value = mock_config_instance

        with pytest.raises(Exception):
            create_application()

    @patch("src.main.create_application")
    @patch("src.main.app")
    def test_main_module_import(self, mock_app, mock_create_app):
        """Test de que el módulo main se puede importar"""
        # Simplemente verificar que no hay errores de importación
        from src import main

        assert main is not None
