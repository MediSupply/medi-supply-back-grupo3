"""
Tests unitarios para los DTOs del módulo de productos
"""

from datetime import datetime
import pytest

from src.aplicacion.dtos.producto_dto import ProductoDto


class TestProductoDto:
    """Tests para el ProductoDto"""

    def test_producto_dto_creation(self, sample_producto_dto):
        """Test de creación del ProductoDto"""
        assert sample_producto_dto.id == "prod-001"
        assert sample_producto_dto.nombre == "Laptop"
        assert sample_producto_dto.descripcion == "Laptop gaming de alta gama"
        assert sample_producto_dto.valor_unitario == 1500.00
        assert sample_producto_dto.categoria == "electronicos"
        assert sample_producto_dto.cantidad_disponible == 10
        assert sample_producto_dto.condiciones_almacenamiento == "Temperatura ambiente"
        assert sample_producto_dto.lote == "LOT-001"
        assert sample_producto_dto.tiempo_estimado_entrega == "5 días"
        assert sample_producto_dto.id_proveedor == "prov-001"

    def test_producto_dto_immutable(self, sample_producto_dto):
        """Test de que ProductoDto es inmutable"""
        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            sample_producto_dto.nombre = "Nueva Laptop"

    def test_producto_dto_different_categories(self):
        """Test de diferentes categorías"""
        # Test ELECTRONICOS
        laptop = ProductoDto(
            id="prod-004",
            nombre="Smartphone",
            descripcion="Teléfono inteligente",
            categoria="electronicos",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=800.00,
            cantidad_disponible=15,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-004",
            tiempo_estimado_entrega="3 días",
            id_proveedor="prov-001",
            ubicacion="Almacén B - Estante 1",
        )
        assert laptop.categoria == "electronicos"

        # Test DEPORTES
        pelota = ProductoDto(
            id="prod-005",
            nombre="Pelota de fútbol",
            descripcion="Pelota oficial",
            categoria="deportes",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=30.00,
            cantidad_disponible=25,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-005",
            tiempo_estimado_entrega="2 días",
            id_proveedor="prov-002",
            ubicacion="Almacén C - Estante 5",
        )
        assert pelota.categoria == "deportes"

        # Test OTROS
        misc = ProductoDto(
            id="prod-006",
            nombre="Producto Varios",
            descripcion="Producto misceláneo",
            categoria="otros",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=10.00,
            cantidad_disponible=100,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-006",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-003",
            ubicacion="Almacén D - Estante 2",
        )
        assert misc.categoria == "otros"

    def test_producto_dto_float_precision(self):
        """Test de precisión float en precios"""
        producto_dto = ProductoDto(
            id="prod-007",
            nombre="Producto Preciso",
            descripcion="Producto con precio preciso",
            categoria="otros",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=99.99,
            cantidad_disponible=1,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-007",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-001",
            ubicacion="Almacén A - Estante 1",
        )

        assert producto_dto.valor_unitario == 99.99
        assert isinstance(producto_dto.valor_unitario, float)

    def test_producto_dto_zero_stock(self):
        """Test de producto con stock cero"""
        producto_dto = ProductoDto(
            id="prod-009",
            nombre="Producto Agotado",
            descripcion="Producto sin stock",
            categoria="hogar",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=25.00,
            cantidad_disponible=0,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-009",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-001",
            ubicacion="Almacén A - Estante 4",
        )

        assert producto_dto.cantidad_disponible == 0

    def test_producto_dto_with_different_providers(self):
        """Test de productos con diferentes proveedores"""
        producto1 = ProductoDto(
            id="prod-010",
            nombre="Producto 1",
            descripcion="Descripción",
            categoria="otros",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=100.00,
            cantidad_disponible=10,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-010",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-001",
            ubicacion="Almacén A - Estante 1",
        )

        producto2 = ProductoDto(
            id="prod-011",
            nombre="Producto 2",
            descripcion="Descripción",
            categoria="otros",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=200.00,
            cantidad_disponible=20,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-011",
            tiempo_estimado_entrega="2 días",
            id_proveedor="prov-002",
            ubicacion="Almacén B - Estante 2",
        )

        assert producto1.id_proveedor == "prov-001"
        assert producto2.id_proveedor == "prov-002"
