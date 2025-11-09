"""
Tests unitarios para la interfaz ProductoRepository
"""

import pytest

from src.dominio.repositorios.producto_repository import ProductoRepository


class TestProductoRepositoryInterface:
    """Tests para la interfaz ProductoRepository"""

    def test_repository_is_abstract(self):
        """Test de que ProductoRepository es una clase abstracta"""
        # Verificar que no se puede instanciar directamente
        with pytest.raises(TypeError):
            ProductoRepository()

    def test_repository_has_abstract_methods(self):
        """Test de que ProductoRepository tiene los métodos abstractos correctos"""
        # Verificar que los métodos abstractos existen
        assert hasattr(ProductoRepository, 'obtener_todos')
        assert hasattr(ProductoRepository, 'obtener_por_id')
        assert hasattr(ProductoRepository, 'obtener_por_categoria')
        assert hasattr(ProductoRepository, 'buscar_por_nombre')
        
        # Verificar que son métodos abstractos usando ABC
        from abc import ABC
        assert issubclass(ProductoRepository, ABC)
        
        # Verificar que los métodos están marcados como abstractos
        import inspect
        abstract_methods = ProductoRepository.__abstractmethods__
        assert 'obtener_todos' in abstract_methods
        assert 'obtener_por_id' in abstract_methods
        assert 'obtener_por_categoria' in abstract_methods
        assert 'buscar_por_nombre' in abstract_methods

