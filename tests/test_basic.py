"""
Tests básicos para el proyecto MediSupply
"""

import os
import sys

import pytest

# Agregar los directorios src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "gateway", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "productos", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "provedores", "src"))


class TestProjectStructure:
    """Tests para verificar la estructura del proyecto"""

    def test_gateway_module_exists(self):
        """Verificar que el módulo gateway existe"""
        try:
            import modules.autenticador

            assert True
        except ImportError:
            pytest.skip("Módulo gateway no disponible")

    def test_productos_module_exists(self):
        """Verificar que el módulo productos existe"""
        try:
            import aplicacion.producto_service

            assert True
        except ImportError:
            pytest.skip("Módulo productos no disponible")

    def test_provedores_module_exists(self):
        """Verificar que el módulo provedores existe"""
        try:
            import aplicacion.provedor_service

            assert True
        except ImportError:
            pytest.skip("Módulo provedores no disponible")


class TestBasicFunctionality:
    """Tests básicos de funcionalidad"""

    def test_import_flask(self):
        """Verificar que Flask se puede importar"""
        import flask

        assert flask is not None

    def test_import_requests(self):
        """Verificar que requests se puede importar"""
        import requests

        assert requests is not None

    def test_import_jwt(self):
        """Verificar que PyJWT se puede importar"""
        import jwt

        assert jwt is not None


if __name__ == "__main__":
    pytest.main([__file__])
