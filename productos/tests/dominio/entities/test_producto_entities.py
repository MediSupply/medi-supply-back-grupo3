"""
Tests unitarios para las entidades del módulo de productos
"""

import os
import sys
from decimal import Decimal

import pytest

# Agregar el directorio de productos al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestProductoEntity:
    """Tests para la entidad Producto"""

    def test_producto_entity_creation(self):
        """Test de creación de la entidad Producto"""
        from src.dominio.entities.producto import Categoria, Producto

        producto = Producto(
            id="prod-001",
            nombre="Laptop",
            descripcion="Laptop gaming de alta gama",
            precio=Decimal("1500.00"),
            categoria=Categoria.ELECTRONICOS,
            stock=10,
            activo=True,
        )

        assert producto.id == "prod-001"
        assert producto.nombre == "Laptop"
        assert producto.descripcion == "Laptop gaming de alta gama"
        assert producto.precio == Decimal("1500.00")
        assert producto.categoria == Categoria.ELECTRONICOS
        assert producto.stock == 10
        assert producto.activo is True

    def test_producto_entity_default_active(self):
        """Test de creación con activo por defecto"""
        from src.dominio.entities.producto import Categoria, Producto

        producto = Producto(
            id="prod-002",
            nombre="Camiseta",
            descripcion="Camiseta de algodón",
            precio=Decimal("25.99"),
            categoria=Categoria.ROPA,
            stock=50,
        )

        assert producto.activo is True  # Valor por defecto

    def test_producto_entity_to_dict(self):
        """Test del método to_dict de Producto"""
        from src.dominio.entities.producto import Categoria, Producto

        producto = Producto(
            id="prod-003",
            nombre="Libro",
            descripcion="Libro de programación",
            precio=Decimal("45.50"),
            categoria=Categoria.LIBROS,
            stock=20,
            activo=True,
        )

        producto_dict = producto.to_dict()
        assert isinstance(producto_dict, dict)
        assert producto_dict["id"] == "prod-003"
        assert producto_dict["nombre"] == "Libro"
        assert producto_dict["descripcion"] == "Libro de programación"
        assert producto_dict["precio"] == 45.50  # Convertido a float
        assert producto_dict["categoria"] == "libros"
        assert producto_dict["stock"] == 20
        assert producto_dict["activo"] is True

    def test_producto_entity_immutable(self):
        """Test de que Producto es inmutable"""
        from src.dominio.entities.producto import Categoria, Producto

        producto = Producto(
            id="prod-004",
            nombre="Mesa",
            descripcion="Mesa de madera",
            precio=Decimal("200.00"),
            categoria=Categoria.HOGAR,
            stock=5,
        )

        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            producto.nombre = "Nueva Mesa"

    def test_producto_categoria_enum(self):
        """Test de los valores del enum Categoria"""
        from src.dominio.entities.producto import Categoria

        assert Categoria.ELECTRONICOS.value == "electronicos"
        assert Categoria.ROPA.value == "ropa"
        assert Categoria.HOGAR.value == "hogar"
        assert Categoria.DEPORTES.value == "deportes"
        assert Categoria.LIBROS.value == "libros"
        assert Categoria.OTROS.value == "otros"

    def test_producto_different_categories(self):
        """Test de diferentes categorías"""
        from src.dominio.entities.producto import Categoria, Producto

        # Test ELECTRONICOS
        laptop = Producto(
            id="prod-005",
            nombre="Smartphone",
            descripcion="Teléfono inteligente",
            precio=Decimal("800.00"),
            categoria=Categoria.ELECTRONICOS,
            stock=15,
        )
        assert laptop.categoria == Categoria.ELECTRONICOS

        # Test DEPORTES
        pelota = Producto(
            id="prod-006",
            nombre="Pelota de fútbol",
            descripcion="Pelota oficial",
            precio=Decimal("30.00"),
            categoria=Categoria.DEPORTES,
            stock=25,
        )
        assert pelota.categoria == Categoria.DEPORTES

        # Test OTROS
        misc = Producto(
            id="prod-007",
            nombre="Producto Varios",
            descripcion="Producto misceláneo",
            precio=Decimal("10.00"),
            categoria=Categoria.OTROS,
            stock=100,
        )
        assert misc.categoria == Categoria.OTROS

    def test_producto_decimal_precision(self):
        """Test de precisión decimal en precios"""
        from src.dominio.entities.producto import Categoria, Producto

        producto = Producto(
            id="prod-008",
            nombre="Producto Preciso",
            descripcion="Producto con precio preciso",
            precio=Decimal("99.99"),
            categoria=Categoria.OTROS,
            stock=1,
        )

        assert producto.precio == Decimal("99.99")
        assert float(producto.precio) == 99.99

    def test_producto_inactive(self):
        """Test de producto inactivo"""
        from src.dominio.entities.producto import Categoria, Producto

        producto = Producto(
            id="prod-009",
            nombre="Producto Descontinuado",
            descripcion="Producto que ya no se vende",
            precio=Decimal("50.00"),
            categoria=Categoria.OTROS,
            stock=0,
            activo=False,
        )

        assert producto.activo is False
        assert producto.stock == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
