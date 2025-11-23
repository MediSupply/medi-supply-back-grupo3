"""
Tests unitarios para la configuración de la aplicación
"""

import os
from unittest.mock import MagicMock, Mock, patch

import pytest
from flask import Flask
from src.infraestructura.config.config import Config


class TestConfig:
    """Tests para la clase Config"""

    def test_config_init(self):
        """Test de inicialización de Config"""
        config = Config()
        assert config.app is None

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_create_app(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de creación de aplicación Flask"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        # Set environment variables
        with patch.dict(
            os.environ,
            {
                "ENV": "test",
                "DEBUG": "True",
                "HOST": "127.0.0.1",
                "PORT": "5003",
                "LOG_LEVEL": "DEBUG",
                "JWT_SECRET": "test-secret-key-32-chars-long",
                "ALGORITHM": "HS256",
                "DATABASE_URL": "sqlite:///:memory:",
            },
        ):
            config = Config()
            app = config.create_app()

        assert app is not None
        assert isinstance(app, Flask)
        assert config.app is not None
        # load_dotenv se llama a nivel de módulo, no dentro de create_app
        mock_init_db.assert_called_once()
        mock_create_producto_routes.assert_called_once()
        mock_create_auth_routes.assert_called_once()

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_create_app_with_defaults(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de creación de aplicación con valores por defecto"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        # Remove environment variables to test defaults
        # Necesitamos eliminar las variables, no establecerlas a cadenas vacías
        env_vars_to_remove = ["ENV", "DEBUG", "HOST", "PORT", "LOG_LEVEL", "JWT_SECRET", "ALGORITHM", "DATABASE_URL"]
        original_env = {}
        for var in env_vars_to_remove:
            if var in os.environ:
                original_env[var] = os.environ[var]
                del os.environ[var]

        try:
            config = Config()
            app = config.create_app()

            assert app is not None
            assert app.config["ENV"] == "development"
            assert app.config["DEBUG"] is False
            assert app.config["HOST"] == "0.0.0.0"
            assert app.config["PORT"] == 5002
        finally:
            # Restaurar variables de entorno originales
            for var, value in original_env.items():
                os.environ[var] = value

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_get_app(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de get_app"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        assert config.get_app() is None

        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()
            assert config.get_app() is not None
            assert config.get_app() == app

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_configure_app(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de _configure_app"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        with patch.dict(
            os.environ,
            {
                "ENV": "production",
                "DEBUG": "False",
                "HOST": "0.0.0.0",
                "PORT": "8080",
                "LOG_LEVEL": "WARNING",
                "JWT_SECRET": "production-secret-key-32-chars-long",
                "ALGORITHM": "HS512",
                "DATABASE_URL": "postgresql://user:pass@localhost/db",
            },
        ):
            config = Config()
            app = config.create_app()

        assert app.config["ENV"] == "production"
        assert app.config["DEBUG"] is False
        assert app.config["HOST"] == "0.0.0.0"
        assert app.config["PORT"] == 8080
        assert app.config["LOG_LEVEL"] == "WARNING"
        assert app.config["JWT_SECRET"] == "production-secret-key-32-chars-long"
        assert app.config["ALGORITHM"] == "HS512"
        assert app.config["SQLALCHEMY_DATABASE_URI"] == "postgresql://user:pass@localhost/db"
        assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    @patch("src.infraestructura.config.config.CORS")
    def test_configure_cors(
        self,
        mock_cors,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de _configure_cors"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()

        mock_cors.assert_called_once()
        call_args = mock_cors.call_args
        assert call_args[0][0] == app
        assert call_args[1]["origins"] == ["http://localhost:4200", "http://127.0.0.1:4200"]
        assert call_args[1]["methods"] == ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        assert call_args[1]["allow_headers"] == ["Content-Type", "Authorization"]
        assert call_args[1]["supports_credentials"] is True

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_configure_db(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de _configure_db"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()

        mock_init_db.assert_called_once_with(app)
        mock_db.create_all.assert_called_once()

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_register_routes(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de _register_routes"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()

        # Verificar que se crearon las rutas
        mock_create_producto_routes.assert_called_once()
        mock_create_auth_routes.assert_called_once()
        mock_create_auth_middleware.assert_called_once()

        # Verificar que las rutas están registradas (los blueprints se registran en el app)
        # Los mocks pueden no registrar realmente los blueprints, así que verificamos que se llamaron
        assert mock_create_producto_routes.called
        assert mock_create_auth_routes.called

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_root_route(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de ruta raíz /"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()
            client = app.test_client()

            response = client.get("/")
            assert response.status_code == 200
            data = response.get_json()
            assert data["message"] == "Microservicio de Productos is running"
            assert data["version"] == "2.0.0"
            assert data["auth_middleware"] is True
            assert "auth_endpoints" in data
            assert "permissions" in data

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_health_route(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de ruta /health"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()
            client = app.test_client()

            response = client.get("/health")
            assert response.status_code == 200
            data = response.get_json()
            assert data["status"] == "healthy"
            assert data["service"] == "productos"
            assert data["version"] == "2.0.0"
            assert data["auth_enabled"] is True

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_request_logging(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de logging de requests"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {"DEBUG": "True"}, clear=False):
            app = config.create_app()
            client = app.test_client()

            # Hacer una petición para activar el logging
            response = client.get("/health")
            assert response.status_code == 200

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_request_logging_with_json_body(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de logging de requests con JSON body (cubre línea 110)"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {"DEBUG": "True"}, clear=False):
            app = config.create_app()
            client = app.test_client()

            # Hacer una petición POST con JSON para activar el logging del body
            response = client.post("/health", json={"test": "data"})
            assert response.status_code in [200, 404, 405]  # Puede ser cualquier código

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_response_logging_without_start_time(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de logging de response sin start_time (cubre línea 121)"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()

            # Para cubrir la línea 121, necesitamos que g no tenga start_time
            # Esto puede pasar si el before_request no se ejecuta o falla
            from flask import Response, g

            # Obtener el after_request handler
            after_request_handlers = app.after_request_funcs.get(None, [])
            if after_request_handlers:
                # Crear una respuesta de prueba
                test_response = Response("test", status=200)

                # Ejecutar el handler sin start_time en g
                with app.app_context():
                    # Asegurarnos de que g no tiene start_time
                    if hasattr(g, "start_time"):
                        delattr(g, "start_time")

                    # Ejecutar el handler after_request directamente
                    handler = after_request_handlers[0]
                    result_response = handler(test_response)

                    assert result_response.status_code == 200

    @patch("src.infraestructura.config.config.load_dotenv")
    @patch("src.infraestructura.config.config.init_db_productos")
    @patch("src.infraestructura.config.config.db_productos")
    @patch("src.infraestructura.config.config.create_authorization_middleware")
    @patch("src.infraestructura.config.config.create_authorization_module")
    @patch("src.infraestructura.config.config.create_producto_routes")
    @patch("src.modules.autorizador.infraestructura.rutas.auth_routes.create_auth_routes")
    @patch("src.modules.autorizador.aplicacion.servicios.auth_service.AuthService")
    @patch("src.modules.autorizador.infraestructura.cmd.auth_cmd.AuthCmd")
    def test_setup_dependencies(
        self,
        mock_auth_cmd,
        mock_auth_service,
        mock_create_auth_routes,
        mock_create_producto_routes,
        mock_create_auth_module,
        mock_create_auth_middleware,
        mock_db,
        mock_init_db,
        mock_load_dotenv,
    ):
        """Test de _setup_dependencies"""
        # Setup mocks
        mock_db.create_all = MagicMock()
        mock_init_db.return_value = None
        mock_create_auth_module.return_value = MagicMock()
        mock_create_auth_middleware.return_value = None
        mock_producto_routes = MagicMock()
        mock_create_producto_routes.return_value = mock_producto_routes
        mock_auth_routes = MagicMock()
        mock_create_auth_routes.return_value = mock_auth_routes
        mock_auth_service_instance = MagicMock()
        mock_auth_service.return_value = mock_auth_service_instance
        mock_auth_cmd_instance = MagicMock()
        mock_auth_cmd.return_value = mock_auth_cmd_instance

        config = Config()
        with patch.dict(os.environ, {}, clear=True):
            app = config.create_app()

        # Verificar que se crearon las dependencias
        assert hasattr(config, "producto_controller")
        assert hasattr(config, "authorization_service")
        mock_create_auth_module.assert_called_once()
