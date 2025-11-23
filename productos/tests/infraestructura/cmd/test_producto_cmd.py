"""
Tests unitarios para ProductoCmd
"""

from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest

from src.infraestructura.cmd.producto_cmd import ProductoCmd
from src.dominio.entities.producto import Producto


class TestProductoCmd:
    """Tests para ProductoCmd"""

    @patch('src.infraestructura.cmd.producto_cmd.ProductoMapper')
    def test_obtener_todos_los_productos_exitoso(self, mock_mapper, app_context):
        """Test de obtener todos los productos exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
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
            ),
        ]
        mock_use_case.obtener_todos_los_productos.return_value = productos
        
        mock_dto = MagicMock()
        mock_json = {"id": "prod-001", "nombre": "Producto 1"}
        mock_mapper.entity_to_dto.return_value = mock_dto
        mock_mapper.dto_to_json.return_value = mock_json
        
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_todos_los_productos()

        # Assert
        assert status_code == 200
        mock_use_case.obtener_todos_los_productos.assert_called_once()

    def test_obtener_todos_los_productos_error(self, app_context):
        """Test de obtener todos los productos con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_todos_los_productos.side_effect = Exception("Error de base de datos")
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_todos_los_productos()

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

    @patch('src.infraestructura.cmd.producto_cmd.ProductoMapper')
    def test_obtener_producto_por_id_exitoso(self, mock_mapper, app_context):
        """Test de obtener producto por ID exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
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
        )
        mock_use_case.obtener_producto_por_id.return_value = producto
        
        mock_dto = MagicMock()
        mock_json = {"id": "prod-001", "nombre": "Producto 1"}
        mock_mapper.entity_to_dto.return_value = mock_dto
        mock_mapper.dto_to_json.return_value = mock_json
        
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_producto_por_id("prod-001")

        # Assert
        assert status_code == 200
        mock_use_case.obtener_producto_por_id.assert_called_once_with("prod-001")

    def test_obtener_producto_por_id_no_encontrado(self, app_context):
        """Test de obtener producto por ID cuando no existe"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_producto_por_id.return_value = None
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_producto_por_id("prod-999")

        # Assert
        assert status_code == 404
        assert "error" in response.get_json()
        mock_use_case.obtener_producto_por_id.assert_called_once_with("prod-999")

    def test_obtener_producto_por_id_error(self, app_context):
        """Test de obtener producto por ID con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_producto_por_id.side_effect = Exception("Error de base de datos")
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_producto_por_id("prod-001")

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

    @patch('src.infraestructura.cmd.producto_cmd.ProductoMapper')
    def test_obtener_productos_por_categoria_exitoso(self, mock_mapper, app_context):
        """Test de obtener productos por categoría exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
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
            ),
        ]
        mock_use_case.obtener_productos_por_categoria.return_value = productos
        
        mock_dto = MagicMock()
        mock_json = {"id": "prod-001", "nombre": "Laptop"}
        mock_mapper.entity_to_dto.return_value = mock_dto
        mock_mapper.dto_to_json.return_value = mock_json
        
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_productos_por_categoria("electronicos")

        # Assert
        assert status_code == 200
        mock_use_case.obtener_productos_por_categoria.assert_called_once_with("electronicos")

    def test_obtener_productos_por_categoria_error(self, app_context):
        """Test de obtener productos por categoría con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_productos_por_categoria.side_effect = Exception("Error de base de datos")
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_productos_por_categoria("electronicos")

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

    @patch('src.infraestructura.cmd.producto_cmd.ProductoMapper')
    def test_buscar_productos_por_nombre_exitoso(self, mock_mapper, app_context):
        """Test de buscar productos por nombre exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
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
            ),
        ]
        mock_use_case.buscar_productos_por_nombre.return_value = productos
        
        mock_dto = MagicMock()
        mock_json = {"id": "prod-001", "nombre": "Laptop Gaming"}
        mock_mapper.entity_to_dto.return_value = mock_dto
        mock_mapper.dto_to_json.return_value = mock_json
        
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.buscar_productos_por_nombre("Laptop")

        # Assert
        assert status_code == 200
        mock_use_case.buscar_productos_por_nombre.assert_called_once_with("Laptop")

    def test_buscar_productos_por_nombre_error(self, app_context):
        """Test de buscar productos por nombre con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.buscar_productos_por_nombre.side_effect = Exception("Error de base de datos")
        cmd = ProductoCmd(mock_use_case)

        # Act
        response, status_code = cmd.buscar_productos_por_nombre("Laptop")

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

