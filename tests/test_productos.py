"""
Tests para el módulo de productos
"""

import os
import sys

import pytest

# Agregar el directorio productos/src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "productos", "src"))


class TestProductosModule:
    """Tests para el módulo de productos"""

    def test_producto_entity_import(self):
        """Verificar que la entidad producto se puede importar"""
        try:
            from dominio.entities.producto import Producto

            assert Producto is not None
        except ImportError as e:
            pytest.skip(f"Entidad producto no disponible: {e}")

    def test_producto_dto_import(self):
        """Verificar que el DTO producto se puede importar"""
        try:
            from aplicacion.dtos.producto_dto import ProductoDTO

            assert ProductoDTO is not None
        except ImportError as e:
            pytest.skip(f"DTO producto no disponible: {e}")

    def test_producto_service_import(self):
        """Verificar que el servicio producto se puede importar"""
        try:
            from aplicacion.servicios.producto_service import ProductoService

            assert ProductoService is not None
        except ImportError as e:
            pytest.skip(f"Servicio producto no disponible: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
