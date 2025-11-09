"""
Tests unitarios para el servicio de clientes
"""

import os
import sys
from unittest.mock import MagicMock

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteService:
    """Tests para ClienteService"""

    @pytest.fixture
    def mock_repository(self):
        """Fixture para crear un mock del repositorio"""
        return MagicMock()

    @pytest.fixture
    def cliente_service(self, mock_repository):
        """Fixture para crear una instancia del servicio"""
        from src.aplicacion.servicios.cliente_service import ClienteService

        return ClienteService(mock_repository)

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

    def test_obtener_todos_los_clientes(self, cliente_service, mock_repository, sample_cliente):
        """Test de obtener todos los clientes"""
        mock_repository.obtener_todos.return_value = [sample_cliente]

        clientes = cliente_service.obtener_todos_los_clientes()

        assert len(clientes) == 1
        assert clientes[0].id == "cli-001"
        mock_repository.obtener_todos.assert_called_once()

    def test_obtener_cliente_por_id(self, cliente_service, mock_repository, sample_cliente):
        """Test de obtener cliente por ID"""
        mock_repository.obtener_por_id.return_value = sample_cliente

        cliente = cliente_service.obtener_cliente_por_id("cli-001")

        assert cliente is not None
        assert cliente.id == "cli-001"
        mock_repository.obtener_por_id.assert_called_once_with("cli-001")

    def test_obtener_cliente_por_id_no_encontrado(self, cliente_service, mock_repository):
        """Test de obtener cliente por ID cuando no existe"""
        mock_repository.obtener_por_id.return_value = None

        cliente = cliente_service.obtener_cliente_por_id("cli-inexistente")

        assert cliente is None

    def test_obtener_clientes_por_categoria(self, cliente_service, mock_repository):
        """Test de obtener clientes por categoría"""
        # Clientes no tienen categoría, debería retornar lista vacía
        mock_repository.obtener_por_categoria.return_value = []

        clientes = cliente_service.obtener_clientes_por_categoria("cualquiera")

        assert len(clientes) == 0
        mock_repository.obtener_por_categoria.assert_called_once_with("cualquiera")

    def test_buscar_clientes_por_nombre(self, cliente_service, mock_repository, sample_cliente):
        """Test de búsqueda por nombre"""
        mock_repository.buscar_por_nombre.return_value = [sample_cliente]

        clientes = cliente_service.buscar_clientes_por_nombre("Hospital")

        assert len(clientes) == 1
        assert "Hospital" in clientes[0].nombre
        mock_repository.buscar_por_nombre.assert_called_once_with("Hospital")

    def test_crear_cliente(self, cliente_service, mock_repository, sample_cliente):
        """Test de crear cliente"""
        mock_repository.crear.return_value = sample_cliente

        cliente_creado = cliente_service.crear_cliente(sample_cliente)

        assert cliente_creado is not None
        assert cliente_creado.id == "cli-001"
        mock_repository.crear.assert_called_once_with(sample_cliente)

    def test_obtener_clientes_por_categoria_with_value_error(self, cliente_service, mock_repository):
        """Test de obtener clientes por categoría cuando el repositorio lanza ValueError"""
        mock_repository.obtener_por_categoria.side_effect = ValueError("Categoría inválida")

        clientes = cliente_service.obtener_clientes_por_categoria("invalid")

        assert len(clientes) == 0
        assert clientes == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

