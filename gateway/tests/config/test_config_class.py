"""
Tests unitarios para la clase Config del gateway
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))


class TestConfig:
    """Tests para la clase Config"""

    @patch("config.config.init_db")
    @patch("config.config.db")
    def test_config_initialization(self, mock_db, mock_init_db):
        """Test de inicialización de Config"""
        from config.config import Config

        config = Config()
        assert config.app is None

    @patch("config.config.init_db")
    @patch("config.config.db")
    @patch("config.config.create_health_routes")
    @patch("config.config.create_auth_routes")
    @patch("config.config.create_producto_routes")
    @patch("config.config.create_provedores_routes")
    @patch("config.config.create_cliente_routes")
    def test_create_app(
        self,
        mock_cliente_routes,
        mock_provedores_routes,
        mock_producto_routes,
        mock_auth_routes,
        mock_health_routes,
        mock_db,
        mock_init_db,
    ):
        """Test de create_app"""
        from config.config import Config

        config = Config()
        app = config.create_app()

        assert app is not None
        assert config.app == app
        mock_init_db.assert_called_once()

    @patch("config.config.init_db")
    @patch("config.config.db")
    def test_configure_app(self, mock_db, mock_init_db):
        """Test de _configure_app"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)
        config._configure_app()

        assert config.app.config["ENV"] is not None
        assert "DEBUG" in config.app.config
        assert "HOST" in config.app.config
        assert "PORT" in config.app.config

    @patch("config.config.init_db")
    @patch("config.config.db")
    @patch("config.config.CORS")
    def test_configure_cors(self, mock_cors, mock_db, mock_init_db):
        """Test de _configure_cors"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)
        config._configure_cors()

        mock_cors.assert_called_once()

    @patch("config.config.init_db")
    @patch("config.config.db")
    def test_configure_db(self, mock_db, mock_init_db):
        """Test de _configure_db"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)
        config.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        config._configure_db()

        mock_init_db.assert_called_once_with(config.app)

    @patch("config.config.init_db")
    @patch("config.config.db")
    def test_configure_request_logging(self, mock_db, mock_init_db):
        """Test de _configure_request_logging"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)
        config.app.config["DEBUG"] = False
        config._configure_request_logging()

        # Verificar que se configuraron los decoradores
        assert len(config.app.before_request_funcs) > 0
        assert len(config.app.after_request_funcs) > 0

    @patch("config.config.init_db")
    @patch("config.config.db")
    def test_configure_external_services(self, mock_db, mock_init_db):
        """Test de _configure_external_services"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)
        # Este método actualmente no hace nada (solo tiene ...)
        config._configure_external_services()
        # Solo verificamos que no lanza excepción
        assert True

    @patch("config.config.init_db")
    @patch("config.config.db")
    @patch("config.config.HealthRepositoryImpl")
    @patch("config.config.HealthService")
    @patch("config.config.HealthUseCase")
    @patch("config.config.HealthCmd")
    @patch("config.config.AuthRepositoryImpl")
    @patch("config.config.AuthService")
    @patch("config.config.AuthUseCase")
    @patch("config.config.AuthCmd")
    def test_setup_dependencies(
        self,
        mock_auth_cmd,
        mock_auth_use_case,
        mock_auth_service,
        mock_auth_repo,
        mock_health_cmd,
        mock_health_use_case,
        mock_health_service,
        mock_health_repo,
        mock_db,
        mock_init_db,
    ):
        """Test de _setup_dependencies"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)
        config.app.config["JWT_SECRET"] = "test-secret"
        config.app.config["ALGORITHM"] = "HS256"
        config._setup_dependencies()

        assert hasattr(config, "health_controller")
        assert hasattr(config, "auth_controller")

    @patch("config.config.init_db")
    @patch("config.config.db")
    @patch("config.config.create_health_routes")
    @patch("config.config.create_auth_routes")
    @patch("config.config.create_producto_routes")
    @patch("config.config.create_provedores_routes")
    @patch("config.config.create_cliente_routes")
    def test_register_routes(
        self,
        mock_cliente_routes,
        mock_provedores_routes,
        mock_producto_routes,
        mock_auth_routes,
        mock_health_routes,
        mock_db,
        mock_init_db,
    ):
        """Test de _register_routes"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)
        config.health_controller = Mock()
        config.auth_controller = Mock()

        mock_health_bp = Mock()
        mock_auth_bp = Mock()
        mock_producto_bp = Mock()
        mock_provedores_bp = Mock()
        mock_cliente_bp = Mock()

        mock_health_routes.return_value = mock_health_bp
        mock_auth_routes.return_value = mock_auth_bp
        mock_producto_routes.return_value = mock_producto_bp
        mock_provedores_routes.return_value = mock_provedores_bp
        mock_cliente_routes.return_value = mock_cliente_bp

        config._register_routes()

        # Verificar que se llamaron las funciones de creación de rutas
        mock_health_routes.assert_called_once()
        mock_auth_routes.assert_called_once()
        mock_producto_routes.assert_called_once()
        mock_provedores_routes.assert_called_once()
        mock_cliente_routes.assert_called_once()

    @patch("config.config.init_db")
    @patch("config.config.db")
    def test_get_app(self, mock_db, mock_init_db):
        """Test de get_app"""
        from config.config import Config
        from flask import Flask

        config = Config()
        config.app = Flask(__name__)

        app = config.get_app()
        assert app == config.app

    @patch("config.config.init_db")
    @patch("config.config.db")
    def test_get_app_none(self, mock_db, mock_init_db):
        """Test de get_app cuando app es None"""
        from config.config import Config

        config = Config()
        app = config.get_app()
        assert app is None

    @patch("config.config.init_db")
    @patch("config.config.db")
    @patch("config.config.create_health_routes")
    @patch("config.config.create_auth_routes")
    @patch("config.config.create_producto_routes")
    @patch("config.config.create_provedores_routes")
    @patch("config.config.create_cliente_routes")
    def test_root_route(
        self,
        mock_cliente_routes,
        mock_provedores_routes,
        mock_producto_routes,
        mock_auth_routes,
        mock_health_routes,
        mock_db,
        mock_init_db,
    ):
        """Test de la ruta raíz"""
        from config.config import Config

        config = Config()
        config.health_controller = Mock()
        config.auth_controller = Mock()

        mock_health_bp = Mock()
        mock_auth_bp = Mock()
        mock_producto_bp = Mock()
        mock_provedores_bp = Mock()
        mock_cliente_bp = Mock()

        mock_health_routes.return_value = mock_health_bp
        mock_auth_routes.return_value = mock_auth_bp
        mock_producto_routes.return_value = mock_producto_bp
        mock_provedores_routes.return_value = mock_provedores_bp
        mock_cliente_routes.return_value = mock_cliente_bp

        app = config.create_app()
        client = app.test_client()

        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "version" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
