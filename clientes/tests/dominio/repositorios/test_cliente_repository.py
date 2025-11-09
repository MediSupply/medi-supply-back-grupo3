"""
Tests unitarios para el repositorio de clientes (interfaz)
"""

import os
import sys
from abc import ABC

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteRepository:
    """Tests para la interfaz ClienteRepository"""

    def test_repository_is_abstract(self):
        """Test de que ClienteRepository es una clase abstracta"""
        from src.dominio.repositorios.cliente_repository import ClienteRepository

        assert issubclass(ClienteRepository, ABC)

    def test_repository_has_required_methods(self):
        """Test de que ClienteRepository tiene todos los métodos requeridos"""
        from src.dominio.repositorios.cliente_repository import ClienteRepository

        # Verificar que los métodos abstractos existen
        assert hasattr(ClienteRepository, "obtener_todos")
        assert hasattr(ClienteRepository, "obtener_por_id")
        assert hasattr(ClienteRepository, "obtener_por_categoria")
        assert hasattr(ClienteRepository, "buscar_por_nombre")
        assert hasattr(ClienteRepository, "crear")

    def test_repository_cannot_be_instantiated(self):
        """Test de que no se puede instanciar ClienteRepository directamente"""
        from src.dominio.repositorios.cliente_repository import ClienteRepository

        with pytest.raises(TypeError):
            ClienteRepository()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

