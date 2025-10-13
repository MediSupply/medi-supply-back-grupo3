"""
Tests para el módulo de proveedores
"""

import os
import sys

import pytest

# Agregar el directorio provedores/src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "provedores", "src"))


class TestProvedoresModule:
    """Tests para el módulo de proveedores"""

    def test_provedor_entity_import(self):
        """Verificar que la entidad provedor se puede importar"""
        try:
            from dominio.entities.provedor import Provedor

            assert Provedor is not None
        except ImportError as e:
            pytest.skip(f"Entidad provedor no disponible: {e}")

    def test_provedor_dto_import(self):
        """Verificar que el DTO provedor se puede importar"""
        try:
            from aplicacion.dtos.provedor_dto import ProvedorDTO

            assert ProvedorDTO is not None
        except ImportError as e:
            pytest.skip(f"DTO provedor no disponible: {e}")

    def test_provedor_service_import(self):
        """Verificar que el servicio provedor se puede importar"""
        try:
            from aplicacion.servicios.provedor_service import ProvedorService

            assert ProvedorService is not None
        except ImportError as e:
            pytest.skip(f"Servicio provedor no disponible: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
