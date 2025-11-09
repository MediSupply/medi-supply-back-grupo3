"""
Tests unitarios para main.py
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from src.main import create_application, setup_logging


class TestMain:
    """Tests para main.py"""

    @pytest.fixture
    def app(self):
        """Fixture para crear una aplicación Flask"""
        return Flask(__name__)

    def test_setup_logging(self, app):
        """Test de configuración de logging"""
        setup_logging(app)
        # Verificar que no hay errores al configurar logging
        assert app.config.get("LOG_LEVEL") is None or isinstance(app.config.get("LOG_LEVEL"), str)

    @patch('src.main.Config')
    def test_create_application_success(self, mock_config_class):
        """Test de creación exitosa de aplicación"""
        mock_config = MagicMock()
        mock_app = Flask(__name__)
        mock_app.config = {"HOST": "0.0.0.0", "PORT": 5004, "DEBUG": False}
        mock_config.create_app.return_value = mock_app
        mock_config_class.return_value = mock_config

        app = create_application()
        assert app is not None
        assert isinstance(app, Flask)
        mock_config.create_app.assert_called_once()

    @patch('src.main.Config')
    def test_create_application_failure(self, mock_config_class):
        """Test de creación de aplicación con error"""
        mock_config = MagicMock()
        mock_config.create_app.side_effect = Exception("Config error")
        mock_config_class.return_value = mock_config

        with pytest.raises(Exception, match="Config error"):
            create_application()

    def test_main_module_has_app(self):
        """Test de que el módulo main tiene una instancia de app"""
        from src import main
        assert hasattr(main, 'app')
        assert main.app is not None

