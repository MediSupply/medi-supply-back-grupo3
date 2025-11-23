"""
Tests unitarios para los casos de uso de clientes
"""

import os
import sys
from unittest.mock import MagicMock

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteUseCase:
    """Tests para ClienteUseCase"""

    @pytest.fixture
    def mock_service(self):
        """Fixture para crear un mock del servicio"""
        return MagicMock()

    @pytest.fixture
    def cliente_use_case(self, mock_service):
        """Fixture para crear una instancia del caso de uso"""
        from src.aplicacion.use_cases.cliente_use_case import ClienteUseCase

        return ClienteUseCase(mock_service)

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

    def test_obtener_todos_los_clientes(self, cliente_use_case, mock_service, sample_cliente):
        """Test de obtener todos los clientes"""
        mock_service.obtener_todos_los_clientes.return_value = [sample_cliente]

        clientes = cliente_use_case.obtener_todos_los_clientes()

        assert len(clientes) == 1
        assert clientes[0].id == "cli-001"
        mock_service.obtener_todos_los_clientes.assert_called_once()

    def test_obtener_cliente_por_id(self, cliente_use_case, mock_service, sample_cliente):
        """Test de obtener cliente por ID"""
        mock_service.obtener_cliente_por_id.return_value = sample_cliente

        cliente = cliente_use_case.obtener_cliente_por_id("cli-001")

        assert cliente is not None
        assert cliente.id == "cli-001"
        mock_service.obtener_cliente_por_id.assert_called_once_with("cli-001")

    def test_obtener_clientes_por_categoria(self, cliente_use_case, mock_service):
        """Test de obtener clientes por categoría"""
        mock_service.obtener_clientes_por_categoria.return_value = []

        clientes = cliente_use_case.obtener_clientes_por_categoria("cualquiera")

        assert len(clientes) == 0
        mock_service.obtener_clientes_por_categoria.assert_called_once_with("cualquiera")

    def test_buscar_clientes_por_nombre(self, cliente_use_case, mock_service, sample_cliente):
        """Test de búsqueda por nombre"""
        mock_service.buscar_clientes_por_nombre.return_value = [sample_cliente]

        clientes = cliente_use_case.buscar_clientes_por_nombre("Hospital")

        assert len(clientes) == 1
        assert "Hospital" in clientes[0].nombre
        mock_service.buscar_clientes_por_nombre.assert_called_once_with("Hospital")

    def test_crear_cliente(self, cliente_use_case, mock_service, sample_cliente):
        """Test de crear cliente"""
        mock_service.crear_cliente.return_value = sample_cliente

        cliente_creado = cliente_use_case.crear_cliente(sample_cliente)

        assert cliente_creado is not None
        assert cliente_creado.id == "cli-001"
        mock_service.crear_cliente.assert_called_once_with(sample_cliente)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
