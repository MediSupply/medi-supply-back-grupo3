"""
Tests unitarios para Config
"""

from unittest.mock import patch, MagicMock
import pytest
from flask import Flask

from src.infraestructura.config.config import Config


class TestConfig:
    """Tests para Config"""

    @pytest.fixture
    def config(self):
        """Fixture para crear un Config"""
        return Config()

    def test_config_init(self, config):
        """Test de inicialización de Config"""
        assert config.app is None

    @patch('src.infraestructura.config.config.load_dotenv')
    @patch('src.infraestructura.config.config.init_db_provedores')
    @patch('src.infraestructura.config.config.db_provedores')
    def test_create_app(self, mock_db, mock_init_db, mock_dotenv, config):
        """Test de creación de aplicación"""
        mock_db.create_all = MagicMock()
        
        app = config.create_app()
        
        assert app is not None
        assert isinstance(app, Flask)
        assert config.app == app

    @patch('src.infraestructura.config.config.load_dotenv')
    @patch('src.infraestructura.config.config.init_db_provedores')
    @patch('src.infraestructura.config.config.db_provedores')
    def test_configure_app(self, mock_db, mock_init_db, mock_dotenv, config):
        """Test de configuración de aplicación"""
        config.app = Flask(__name__)
        config._configure_app()
        
        assert config.app.config["ENV"] is not None
        assert config.app.config["PORT"] == 5003
        assert "SQLALCHEMY_DATABASE_URI" in config.app.config

    @patch('src.infraestructura.config.config.load_dotenv')
    @patch('src.infraestructura.config.config.init_db_provedores')
    @patch('src.infraestructura.config.config.db_provedores')
    def test_get_app(self, mock_db, mock_init_db, mock_dotenv, config):
        """Test de obtención de aplicación"""
        app = config.create_app()
        assert config.get_app() == app

    @patch('src.infraestructura.config.config.load_dotenv')
    @patch('src.infraestructura.config.config.init_db_provedores')
    @patch('src.infraestructura.config.config.db_provedores')
    def test_register_routes(self, mock_db, mock_init_db, mock_dotenv, config):
        """Test de registro de rutas"""
        app = config.create_app()
        
        # Verificar que las rutas están registradas
        assert "/" in [rule.rule for rule in app.url_map.iter_rules()]
        assert "/health" in [rule.rule for rule in app.url_map.iter_rules()]

