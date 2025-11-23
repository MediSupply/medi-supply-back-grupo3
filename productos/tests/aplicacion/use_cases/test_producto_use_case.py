"""
Tests unitarios para ProductoUseCase
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest
from src.aplicacion.use_cases.producto_use_case import ProductoUseCase
from src.dominio.entities.producto import Producto


class TestProductoUseCase:
    """Tests para ProductoUseCase"""

    def test_obtener_todos_los_productos(self):
        """Test de obtener todos los productos"""
        # Arrange
        mock_service = MagicMock()
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
        ]
        mock_service.obtener_todos_los_productos.return_value = productos
        use_case = ProductoUseCase(mock_service)

        # Act
        result = use_case.obtener_todos_los_productos()

        # Assert
        assert len(result) == 1
        assert result[0].id == "prod-001"
        mock_service.obtener_todos_los_productos.assert_called_once()

    def test_obtener_producto_por_id_existente(self):
        """Test de obtener producto por ID cuando existe"""
        # Arrange
        mock_service = MagicMock()
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
        mock_service.obtener_producto_por_id.return_value = producto
        use_case = ProductoUseCase(mock_service)

        # Act
        result = use_case.obtener_producto_por_id("prod-001")

        # Assert
        assert result is not None
        assert result.id == "prod-001"
        mock_service.obtener_producto_por_id.assert_called_once_with("prod-001")

    def test_obtener_producto_por_id_no_existente(self):
        """Test de obtener producto por ID cuando no existe"""
        # Arrange
        mock_service = MagicMock()
        mock_service.obtener_producto_por_id.return_value = None
        use_case = ProductoUseCase(mock_service)

        # Act
        result = use_case.obtener_producto_por_id("prod-999")

        # Assert
        assert result is None
        mock_service.obtener_producto_por_id.assert_called_once_with("prod-999")

    def test_obtener_productos_por_categoria(self):
        """Test de obtener productos por categoría"""
        # Arrange
        mock_service = MagicMock()
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
        mock_service.obtener_productos_por_categoria.return_value = productos
        use_case = ProductoUseCase(mock_service)

        # Act
        result = use_case.obtener_productos_por_categoria("electronicos")

        # Assert
        assert len(result) == 1
        assert result[0].categoria == "electronicos"
        mock_service.obtener_productos_por_categoria.assert_called_once_with("electronicos")

    def test_buscar_productos_por_nombre(self):
        """Test de buscar productos por nombre"""
        # Arrange
        mock_service = MagicMock()
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
        mock_service.buscar_productos_por_nombre.return_value = productos
        use_case = ProductoUseCase(mock_service)

        # Act
        result = use_case.buscar_productos_por_nombre("Laptop")

        # Assert
        assert len(result) == 1
        assert "Laptop" in result[0].nombre
        mock_service.buscar_productos_por_nombre.assert_called_once_with("Laptop")
