"""
Tests unitarios para las entidades del módulo de productos
"""

from datetime import datetime
import pytest

from src.dominio.entities.producto import Producto


class TestProductoEntity:
    """Tests para la entidad Producto"""

    def test_producto_entity_creation(self, sample_producto):
        """Test de creación de la entidad Producto"""
        assert sample_producto.id == "prod-001"
        assert sample_producto.nombre == "Laptop"
        assert sample_producto.descripcion == "Laptop gaming de alta gama"
        assert sample_producto.valor_unitario == 1500.00
        assert sample_producto.categoria == "electronicos"
        assert sample_producto.cantidad_disponible == 10
        assert sample_producto.condiciones_almacenamiento == "Temperatura ambiente"
        assert sample_producto.lote == "LOT-001"
        assert sample_producto.tiempo_estimado_entrega == "5 días"
        assert sample_producto.id_proveedor == "prov-001"

    def test_producto_entity_to_dict(self, sample_producto):
        """Test del método to_dict de Producto"""
        producto_dict = sample_producto.to_dict()

        assert isinstance(producto_dict, dict)
        assert producto_dict["id"] == "prod-001"
        assert producto_dict["nombre"] == "Laptop"
        assert producto_dict["descripcion"] == "Laptop gaming de alta gama"
        assert producto_dict["valor_unitario"] == 1500.00
        assert producto_dict["categoria"] == "electronicos"
        assert producto_dict["cantidad_disponible"] == 10
        assert producto_dict["condiciones_almacenamiento"] == "Temperatura ambiente"
        assert producto_dict["lote"] == "LOT-001"
        assert producto_dict["tiempo_estimado_entrega"] == "5 días"
        assert producto_dict["id_proveedor"] == "prov-001"
        assert producto_dict["ubicacion"] == "Almacén A - Estante 3"
        assert isinstance(producto_dict["fecha_vencimiento"], datetime)

    def test_producto_entity_immutable(self, sample_producto):
        """Test de que Producto es inmutable"""
        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            sample_producto.nombre = "Nueva Laptop"

    def test_producto_different_categories(self):
        """Test de diferentes categorías"""
        # Test ELECTRONICOS
        laptop = Producto(
            id="prod-005",
            nombre="Smartphone",
            descripcion="Teléfono inteligente",
            categoria="electronicos",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=800.00,
            cantidad_disponible=15,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-005",
            tiempo_estimado_entrega="3 días",
            id_proveedor="prov-001",
            ubicacion="Almacén B - Estante 1",
        )
        assert laptop.categoria == "electronicos"

        # Test DEPORTES
        pelota = Producto(
            id="prod-006",
            nombre="Pelota de fútbol",
            descripcion="Pelota oficial",
            categoria="deportes",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=30.00,
            cantidad_disponible=25,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-006",
            tiempo_estimado_entrega="2 días",
            id_proveedor="prov-002",
            ubicacion="Almacén C - Estante 5",
        )
        assert pelota.categoria == "deportes"

        # Test OTROS
        misc = Producto(
            id="prod-007",
            nombre="Producto Varios",
            descripcion="Producto misceláneo",
            categoria="otros",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=10.00,
            cantidad_disponible=100,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-007",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-003",
            ubicacion="Almacén D - Estante 2",
        )
        assert misc.categoria == "otros"

    def test_producto_float_precision(self):
        """Test de precisión float en precios"""
        producto = Producto(
            id="prod-008",
            nombre="Producto Preciso",
            descripcion="Producto con precio preciso",
            categoria="otros",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=99.99,
            cantidad_disponible=1,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-008",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-001",
            ubicacion="Almacén A - Estante 1",
        )

        assert producto.valor_unitario == 99.99
        assert isinstance(producto.valor_unitario, float)

    def test_producto_zero_stock(self):
        """Test de producto con stock cero"""
        producto = Producto(
            id="prod-009",
            nombre="Producto Agotado",
            descripcion="Producto sin stock",
            categoria="hogar",
            condiciones_almacenamiento="Temperatura ambiente",
            valor_unitario=50.00,
            cantidad_disponible=0,
            fecha_vencimiento=datetime(2025, 12, 31),
            lote="LOT-009",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-001",
            ubicacion="Almacén A - Estante 4",
        )

        assert producto.cantidad_disponible == 0

    def test_producto_with_different_providers(self):
        """Test de productos con diferentes proveedores"""
        producto1 = Producto(
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

        producto2 = Producto(
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
