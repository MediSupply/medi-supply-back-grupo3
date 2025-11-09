"""
Tests unitarios para el controlador de clientes (ClienteCmd)
"""

import os
import sys
from unittest.mock import MagicMock

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteCmd:
    """Tests para ClienteCmd"""

    @pytest.fixture
    def mock_use_case(self):
        """Fixture para crear un mock del caso de uso"""
        return MagicMock()

    @pytest.fixture
    def cliente_cmd(self, mock_use_case, app_context):
        """Fixture para crear una instancia del controlador"""
        from src.infraestructura.cmd.cliente_cmd import ClienteCmd

        return ClienteCmd(mock_use_case)

    @pytest.fixture
    def sample_cliente(self):
        """Fixture para crear un cliente de ejemplo"""
        from src.dominio.entities.cliente import Cliente

        return Cliente(
            id="cli-001",
            nombre="Hospital Test",
            email="test@test.com",
            telefono="+57 1 111 2222",
            direccion="Dirección Test",
            razon_social="Razón Social Test",
            nit="900111222-3",
        )

    def test_obtener_todos_los_clientes(self, cliente_cmd, mock_use_case, sample_cliente):
        """Test de obtener todos los clientes"""
        mock_use_case.obtener_todos_los_clientes.return_value = [sample_cliente]

        response, status_code = cliente_cmd.obtener_todos_los_clientes()

        assert status_code == 200


    def test_obtener_todos_los_clientes_empty(self, cliente_cmd, mock_use_case):
        """Test de obtener todos los clientes cuando no hay ninguno"""
        mock_use_case.obtener_todos_los_clientes.return_value = []

        response, status_code = cliente_cmd.obtener_todos_los_clientes()

        assert status_code == 200


    def test_obtener_todos_los_clientes_error(self, cliente_cmd, mock_use_case):
        """Test de error al obtener todos los clientes"""
        mock_use_case.obtener_todos_los_clientes.side_effect = Exception("Error de base de datos")

        response, status_code = cliente_cmd.obtener_todos_los_clientes()

        assert status_code == 500
        assert "error" in response.json

    def test_obtener_cliente_por_id(self, cliente_cmd, mock_use_case, sample_cliente):
        """Test de obtener cliente por ID"""
        mock_use_case.obtener_cliente_por_id.return_value = sample_cliente

        response, status_code = cliente_cmd.obtener_cliente_por_id("cli-001")

        assert status_code == 200


    def test_obtener_cliente_por_id_not_found(self, cliente_cmd, mock_use_case):
        """Test de obtener cliente por ID cuando no existe"""
        mock_use_case.obtener_cliente_por_id.return_value = None

        response, status_code = cliente_cmd.obtener_cliente_por_id("cli-inexistente")

        assert status_code == 404

    def test_obtener_cliente_por_id_error(self, cliente_cmd, mock_use_case):
        """Test de error al obtener cliente por ID"""
        mock_use_case.obtener_cliente_por_id.side_effect = Exception("Error de conexión")

        response, status_code = cliente_cmd.obtener_cliente_por_id("cli-001")

        assert status_code == 500

    def test_obtener_clientes_por_categoria(self, cliente_cmd, mock_use_case):
        """Test de obtener clientes por categoría"""
        mock_use_case.obtener_clientes_por_categoria.return_value = []

        response, status_code = cliente_cmd.obtener_clientes_por_categoria("hospitales")

        assert status_code == 200

    def test_obtener_clientes_por_categoria_error(self, cliente_cmd, mock_use_case):
        """Test de error al obtener clientes por categoría"""
        mock_use_case.obtener_clientes_por_categoria.side_effect = Exception("Error")

        response, status_code = cliente_cmd.obtener_clientes_por_categoria("hospitales")

        assert status_code == 500

    def test_buscar_clientes_por_nombre(self, cliente_cmd, mock_use_case, sample_cliente):
        """Test de búsqueda de clientes por nombre"""
        mock_use_case.buscar_clientes_por_nombre.return_value = [sample_cliente]

        response, status_code = cliente_cmd.buscar_clientes_por_nombre("Hospital")

        assert status_code == 200


    def test_buscar_clientes_por_nombre_error(self, cliente_cmd, mock_use_case):
        """Test de error al buscar clientes por nombre"""
        mock_use_case.buscar_clientes_por_nombre.side_effect = Exception("Error")

        response, status_code = cliente_cmd.buscar_clientes_por_nombre("Test")

        assert status_code == 500
        assert "error" in response.json

    def test_crear_cliente(self, cliente_cmd, mock_use_case, sample_cliente):
        """Test de crear cliente"""
        mock_use_case.crear_cliente.return_value = sample_cliente

        cliente_data = {
            "nombre": "Hospital Test",
            "email": "test@test.com",
            "telefono": "+57 1 111 2222",
            "direccion": "Dirección Test",
            "razon_social": "Razón Social Test",
            "nit": "900111222-3",
        }

        response, status_code = cliente_cmd.crear_cliente(cliente_data)

        assert status_code == 201
        assert response.json["nombre"] == "Hospital Test"
        mock_use_case.crear_cliente.assert_called_once()

    def test_crear_cliente_missing_field(self, cliente_cmd, mock_use_case):
        """Test de crear cliente con campo faltante"""
        cliente_data = {
            "nombre": "Hospital Test",
            # Falta email
            "telefono": "+57 1 111 2222",
        }

        response, status_code = cliente_cmd.crear_cliente(cliente_data)

        assert status_code == 400
     

    def test_crear_cliente_error(self, cliente_cmd, mock_use_case):
        """Test de error al crear cliente"""
        mock_use_case.crear_cliente.side_effect = Exception("Error de validación")

        cliente_data = {
            "nombre": "Hospital Test",
            "email": "test@test.com",
            "telefono": "+57 1 111 2222",
            "direccion": "Dirección Test",
            "razon_social": "Razón Social Test",
            "nit": "900111222-3",
        }

        response, status_code = cliente_cmd.crear_cliente(cliente_data)

        assert status_code == 500



if __name__ == "__main__":
    pytest.main([__file__, "-v"])

