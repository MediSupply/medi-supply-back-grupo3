"""
Tests unitarios para los DTOs del módulo de productos
"""

import os
import sys

import pytest

# Agregar el directorio de productos al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestProductoDto:
    """Tests para el ProductoDto"""

    def test_producto_dto_creation(self):
        """Test de creación del ProductoDto"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto, ProductoDto

        producto_dto = ProductoDto(
            id="prod-001",
            nombre="Laptop",
            descripcion="Laptop gaming de alta gama",
            precio=1500.00,
            categoria=CategoriaDto.ELECTRONICOS,
            stock=10,
            activo=True,
        )

        assert producto_dto.id == "prod-001"
        assert producto_dto.nombre == "Laptop"
        assert producto_dto.descripcion == "Laptop gaming de alta gama"
        assert producto_dto.precio == 1500.00
        assert producto_dto.categoria == CategoriaDto.ELECTRONICOS
        assert producto_dto.stock == 10
        assert producto_dto.activo is True

    def test_producto_dto_default_active(self):
        """Test de creación con activo por defecto"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto, ProductoDto

        producto_dto = ProductoDto(
            id="prod-002",
            nombre="Camiseta",
            descripcion="Camiseta de algodón",
            precio=25.99,
            categoria=CategoriaDto.ROPA,
            stock=50,
        )

        assert producto_dto.activo is True  # Valor por defecto

    def test_producto_dto_immutable(self):
        """Test de que ProductoDto es inmutable"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto, ProductoDto

        producto_dto = ProductoDto(
            id="prod-003",
            nombre="Libro",
            descripcion="Libro de programación",
            precio=45.50,
            categoria=CategoriaDto.LIBROS,
            stock=20,
        )

        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            producto_dto.nombre = "Nuevo Libro"

    def test_producto_dto_categoria_enum(self):
        """Test de los valores del enum CategoriaDto"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto

        assert CategoriaDto.ELECTRONICOS.value == "electronicos"
        assert CategoriaDto.ROPA.value == "ropa"
        assert CategoriaDto.HOGAR.value == "hogar"
        assert CategoriaDto.DEPORTES.value == "deportes"
        assert CategoriaDto.LIBROS.value == "libros"
        assert CategoriaDto.OTROS.value == "otros"

    def test_producto_dto_different_categories(self):
        """Test de diferentes categorías"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto, ProductoDto

        # Test ELECTRONICOS
        laptop = ProductoDto(
            id="prod-004",
            nombre="Smartphone",
            descripcion="Teléfono inteligente",
            precio=800.00,
            categoria=CategoriaDto.ELECTRONICOS,
            stock=15,
        )
        assert laptop.categoria == CategoriaDto.ELECTRONICOS

        # Test DEPORTES
        pelota = ProductoDto(
            id="prod-005",
            nombre="Pelota de fútbol",
            descripcion="Pelota oficial",
            precio=30.00,
            categoria=CategoriaDto.DEPORTES,
            stock=25,
        )
        assert pelota.categoria == CategoriaDto.DEPORTES

        # Test OTROS
        misc = ProductoDto(
            id="prod-006",
            nombre="Producto Varios",
            descripcion="Producto misceláneo",
            precio=10.00,
            categoria=CategoriaDto.OTROS,
            stock=100,
        )
        assert misc.categoria == CategoriaDto.OTROS

    def test_producto_dto_float_precision(self):
        """Test de precisión float en precios"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto, ProductoDto

        producto_dto = ProductoDto(
            id="prod-007",
            nombre="Producto Preciso",
            descripcion="Producto con precio preciso",
            precio=99.99,
            categoria=CategoriaDto.OTROS,
            stock=1,
        )

        assert producto_dto.precio == 99.99
        assert isinstance(producto_dto.precio, float)

    def test_producto_dto_inactive(self):
        """Test de producto inactivo"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto, ProductoDto

        producto_dto = ProductoDto(
            id="prod-008",
            nombre="Producto Descontinuado",
            descripcion="Producto que ya no se vende",
            precio=50.00,
            categoria=CategoriaDto.OTROS,
            stock=0,
            activo=False,
        )

        assert producto_dto.activo is False
        assert producto_dto.stock == 0

    def test_producto_dto_zero_stock(self):
        """Test de producto con stock cero"""
        from src.aplicacion.dtos.producto_dto import CategoriaDto, ProductoDto

        producto_dto = ProductoDto(
            id="prod-009",
            nombre="Producto Agotado",
            descripcion="Producto sin stock",
            precio=25.00,
            categoria=CategoriaDto.HOGAR,
            stock=0,
            activo=True,
        )

        assert producto_dto.stock == 0
        assert producto_dto.activo is True  # Puede estar activo pero sin stock


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
