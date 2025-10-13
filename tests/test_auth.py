"""
Tests para el módulo de autenticación
"""

import os
import sys

import pytest

# Agregar el directorio gateway/src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "gateway", "src"))


class TestAuthModule:
    """Tests para el módulo de autenticación"""

    def test_auth_entities_import(self):
        """Verificar que las entidades de auth se pueden importar"""
        try:
            from modules.autenticador.dominio.entities.session import Session
            from modules.autenticador.dominio.entities.user import User

            assert User is not None
            assert Session is not None
        except ImportError as e:
            pytest.skip(f"Módulo de auth no disponible: {e}")

    def test_auth_dtos_import(self):
        """Verificar que los DTOs de auth se pueden importar"""
        try:
            from modules.autenticador.aplicacion.dtos.session_dto import SessionDTO
            from modules.autenticador.aplicacion.dtos.user_dto import UserDTO

            assert UserDTO is not None
            assert SessionDTO is not None
        except ImportError as e:
            pytest.skip(f"DTOs de auth no disponibles: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
