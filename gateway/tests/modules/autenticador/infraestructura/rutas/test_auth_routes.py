"""
Tests unitarios para las rutas de autenticación del gateway
"""

import os
import sys
from unittest.mock import Mock

import pytest
from flask import Blueprint, Flask

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestAuthRoutes:
    """Tests para las rutas de autenticación"""

    def setup_method(self):
        """Setup para cada test"""
        from modules.autenticador.infraestructura.rutas.auth_routes import create_auth_routes

        # Crear mock del controlador
        self.mock_controller = Mock()

        # Crear aplicación Flask de prueba
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        
        # Crear blueprint usando la función real
        self.auth_bp = create_auth_routes(self.mock_controller)
        self.app.register_blueprint(self.auth_bp)
        
        self.client = self.app.test_client()

    def test_signup_endpoint_success(self):
        """Test del endpoint signup exitoso"""
        # Mock del controlador
        self.mock_controller.signUp.return_value = ({"session": "data"}, 201)

        # Datos de prueba
        signup_data = {"name": "Test User", "email": "test@example.com", "password": "password123", "role": "USER"}

        # Ejecutar request
        response = self.client.post("/auth/signup", json=signup_data, content_type="application/json")

        # Verificaciones
        assert response.status_code == 201
        self.mock_controller.signUp.assert_called_once_with("Test User", "test@example.com", "password123", "USER")

    def test_signup_endpoint_without_role(self):
        """Test del endpoint signup sin especificar rol (debe usar USER por defecto)"""
        # Mock del controlador
        self.mock_controller.signUp.return_value = ({"session": "data"}, 201)

        # Datos de prueba sin rol
        signup_data = {"name": "Test User", "email": "test@example.com", "password": "password123"}

        # Ejecutar request
        response = self.client.post("/auth/signup", json=signup_data, content_type="application/json")

        # Verificaciones
        assert response.status_code == 201
        self.mock_controller.signUp.assert_called_once_with("Test User", "test@example.com", "password123", "USER")

    def test_signup_endpoint_with_admin_role(self):
        """Test del endpoint signup con rol ADMIN"""
        # Mock del controlador
        self.mock_controller.signUp.return_value = ({"session": "data"}, 201)

        # Datos de prueba con rol ADMIN
        signup_data = {"name": "Admin User", "email": "admin@example.com", "password": "admin123", "role": "ADMIN"}

        # Ejecutar request
        response = self.client.post("/auth/signup", json=signup_data, content_type="application/json")

        # Verificaciones
        assert response.status_code == 201
        self.mock_controller.signUp.assert_called_once_with("Admin User", "admin@example.com", "admin123", "ADMIN")

    def test_signup_endpoint_missing_data(self):
        """Test del endpoint signup con datos faltantes"""
        # Mock del controlador para devolver error
        self.mock_controller.signUp.return_value = ({"error": "Datos faltantes"}, 400)

        # Datos de prueba incompletos
        signup_data = {
            "name": "Test User",
            "email": "test@example.com",
            # Falta password
        }

        # Ejecutar request
        response = self.client.post("/auth/signup", json=signup_data, content_type="application/json")

        # Verificaciones
        assert response.status_code == 400
        self.mock_controller.signUp.assert_called_once()

    def test_signup_endpoint_server_error(self):
        """Test del endpoint signup con error del servidor"""
        # Mock del controlador para devolver error 500
        self.mock_controller.signUp.return_value = ({"error": "Error interno"}, 500)

        # Datos de prueba válidos
        signup_data = {"name": "Test User", "email": "test@example.com", "password": "password123"}

        # Ejecutar request
        response = self.client.post("/auth/signup", json=signup_data, content_type="application/json")

        # Verificaciones
        assert response.status_code == 500
        self.mock_controller.signUp.assert_called_once()

    def test_login_endpoint_success(self):
        """Test del endpoint login exitoso"""
        # Mock del controlador
        self.mock_controller.login.return_value = ({"session": "data"}, 200)

        # Datos de prueba
        login_data = {"email": "test@example.com", "password": "password123"}

        # Ejecutar request
        response = self.client.post("/auth/login", json=login_data, content_type="application/json")

        # Verificaciones
        assert response.status_code == 200
        self.mock_controller.login.assert_called_once_with("test@example.com", "password123")

    def test_signout_endpoint_success(self):
        """Test del endpoint signout exitoso"""
        # Mock del controlador
        self.mock_controller.signOut.return_value = ({"message": "Sesión cerrada"}, 200)

        # Ejecutar request
        response = self.client.post("/auth/signout")

        # Verificaciones
        assert response.status_code == 200
        self.mock_controller.signOut.assert_called_once()

    def test_signup_endpoint_invalid_json(self):
        """Test del endpoint signup con JSON inválido"""
        # Ejecutar request sin JSON válido
        response = self.client.post("/auth/signup", data="invalid json", content_type="application/json")

        # Debe devolver error 400 por JSON inválido
        assert response.status_code == 400

    def test_get_me_endpoint_success(self):
        """Test del endpoint /me exitoso"""
        # Mock del controlador
        self.mock_controller.get_me.return_value = ({"id": "user-id-123", "name": "Test User", "email": "test@example.com", "role": "user"}, 200)

        # Ejecutar request con header Authorization
        response = self.client.get("/auth/me", headers={"Authorization": "Bearer valid-token"})

        # Verificaciones
        assert response.status_code == 200
        self.mock_controller.get_me.assert_called_once()
        response_data = response.get_json()
        assert response_data["id"] == "user-id-123"
        assert response_data["name"] == "Test User"
        assert response_data["email"] == "test@example.com"
        assert response_data["role"] == "user"

    def test_get_me_endpoint_no_authorization(self):
        """Test del endpoint /me sin header Authorization"""
        # Mock del controlador para devolver error 401
        self.mock_controller.get_me.return_value = ({"error": "Token de autorización no proporcionado"}, 401)

        # Ejecutar request sin header Authorization
        response = self.client.get("/auth/me")

        # Verificaciones
        assert response.status_code == 401
        self.mock_controller.get_me.assert_called_once()

    def test_get_me_endpoint_invalid_token(self):
        """Test del endpoint /me con token inválido"""
        # Mock del controlador para devolver error 401
        self.mock_controller.get_me.return_value = ({"error": "Token inválido o expirado"}, 401)

        # Ejecutar request con token inválido
        response = self.client.get("/auth/me", headers={"Authorization": "Bearer invalid-token"})

        # Verificaciones
        assert response.status_code == 401
        self.mock_controller.get_me.assert_called_once()

    def test_get_me_endpoint_invalid_format(self):
        """Test del endpoint /me con formato de token inválido"""
        # Mock del controlador para devolver error 401
        self.mock_controller.get_me.return_value = ({"error": "Formato de token inválido. Use 'Bearer <token>'"}, 401)

        # Ejecutar request con formato inválido (sin "Bearer ")
        response = self.client.get("/auth/me", headers={"Authorization": "invalid-format-token"})

        # Verificaciones
        assert response.status_code == 401
        self.mock_controller.get_me.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
