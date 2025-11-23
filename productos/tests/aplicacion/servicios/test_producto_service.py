"""
Tests unitarios para ProductoService
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest
from src.aplicacion.servicios.producto_service import ProductoService
from src.dominio.entities.producto import Producto


class TestProductoService:
    """Tests para ProductoService"""

    def test_obtener_todos_los_productos(self, mock_producto_repository):
        """Test de obtener todos los productos"""
        # Arrange
        productos = [
            Producto(
                id="prod-001",
                nombre="Producto 1",
                descripcion="Descripción 1",
                categoria="electronicos",
                condiciones_almacenamiento="Temperatura ambiente",
                valor_unitario=100.00,
                cantidad_disponible=10,
                fecha_vencimiento=datetime(2025, 12, 31),
                lote="LOT-001",
                tiempo_estimado_entrega="5 días",
                id_proveedor="prov-001",
                ubicacion="Almacén A - Estante 1",
            ),
            Producto(
                id="prod-002",
                nombre="Producto 2",
                descripcion="Descripción 2",
                categoria="deportes",
                condiciones_almacenamiento="Temperatura ambiente",
                valor_unitario=200.00,
                cantidad_disponible=20,
                fecha_vencimiento=datetime(2025, 12, 31),
                lote="LOT-002",
                tiempo_estimado_entrega="3 días",
                id_proveedor="prov-002",
                ubicacion="Almacén B - Estante 2",
            ),
        ]
        mock_producto_repository.obtener_todos.return_value = productos
        service = ProductoService(mock_producto_repository)

        # Act
        result = service.obtener_todos_los_productos()

        # Assert
        assert len(result) == 2
        assert result[0].id == "prod-001"
        assert result[1].id == "prod-002"
        mock_producto_repository.obtener_todos.assert_called_once()

    def test_obtener_producto_por_id_existente(self, mock_producto_repository):
        """Test de obtener producto por ID cuando existe"""
        # Arrange
        producto = Producto(
            id="prod-001",
            nombre="Producto 1",
            descripcion="Descripción 1",
            categoria="electronicos",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=100.00,
            cantidad_disponible=10,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-001",
            tiempo_estimado_entrega="5 días",
            id_proveedor="prov-001",
            ubicacion="Almacén A - Estante 1",
        )
        mock_producto_repository.obtener_por_id.return_value = producto
        service = ProductoService(mock_producto_repository)

        # Act
        result = service.obtener_producto_por_id("prod-001")

        # Assert
        assert result is not None
        assert result.id == "prod-001"
        assert result.nombre == "Producto 1"
        mock_producto_repository.obtener_por_id.assert_called_once_with("prod-001")

    def test_obtener_producto_por_id_no_existente(self, mock_producto_repository):
        """Test de obtener producto por ID cuando no existe"""
        # Arrange
        mock_producto_repository.obtener_por_id.return_value = None
        service = ProductoService(mock_producto_repository)

        # Act
        result = service.obtener_producto_por_id("prod-999")

        # Assert
        assert result is None
        mock_producto_repository.obtener_por_id.assert_called_once_with("prod-999")

    def test_obtener_productos_por_categoria(self, mock_producto_repository):
        """Test de obtener productos por categoría"""
        # Arrange
        productos = [
            Producto(
                id="prod-001",
                nombre="Laptop",
                descripcion="Laptop gaming",
                categoria="electronicos",
                condiciones_almacenamiento="Temperatura ambiente",
                valor_unitario=1500.00,
                cantidad_disponible=10,
                fecha_vencimiento=datetime(2025, 12, 31),
                lote="LOT-001",
                tiempo_estimado_entrega="5 días",
                id_proveedor="prov-001",
                ubicacion="Almacén A - Estante 3",
            ),
        ]
        mock_producto_repository.obtener_por_categoria.return_value = productos
        service = ProductoService(mock_producto_repository)

        # Act
        result = service.obtener_productos_por_categoria("electronicos")

        # Assert
        assert len(result) == 1
        assert result[0].categoria == "electronicos"
        mock_producto_repository.obtener_por_categoria.assert_called_once_with("electronicos")

    def test_buscar_productos_por_nombre(self, mock_producto_repository):
        """Test de buscar productos por nombre"""
        # Arrange
        productos = [
            Producto(
                id="prod-001",
                nombre="Laptop Gaming",
                descripcion="Laptop gaming de alta gama",
                categoria="electronicos",
                condiciones_almacenamiento="Temperatura ambiente",
                valor_unitario=1500.00,
                cantidad_disponible=10,
                fecha_vencimiento=datetime(2025, 12, 31),
                lote="LOT-001",
                tiempo_estimado_entrega="5 días",
                id_proveedor="prov-001",
                ubicacion="Almacén A - Estante 3",
            ),
        ]
        mock_producto_repository.buscar_por_nombre.return_value = productos
        service = ProductoService(mock_producto_repository)

        # Act
        result = service.buscar_productos_por_nombre("Laptop")

        # Assert
        assert len(result) == 1
        assert "Laptop" in result[0].nombre
        mock_producto_repository.buscar_por_nombre.assert_called_once_with("Laptop")

    def test_buscar_productos_por_nombre_sin_resultados(self, mock_producto_repository):
        """Test de buscar productos por nombre sin resultados"""
        # Arrange
        mock_producto_repository.buscar_por_nombre.return_value = []
        service = ProductoService(mock_producto_repository)

        # Act
        result = service.buscar_productos_por_nombre("Inexistente")

        # Assert
        assert len(result) == 0
        mock_producto_repository.buscar_por_nombre.assert_called_once_with("Inexistente")
