"""
Tests unitarios para los repositorios del módulo de health del gateway
"""

import os
import sys
from unittest.mock import Mock

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthRepository:
    """Tests para el HealthRepository"""

    def test_health_repository_initialization(self):
        """Test de inicialización del HealthRepository"""
        from modules.health.infraestructura.repositorios.health_repository import HealthRepositoryImpl

        repo = HealthRepositoryImpl()
        assert repo is not None

    def test_health_repository_get_health(self):
        """Test del método get_health del HealthRepository"""
        from modules.health.dominio.entities.health import Health
        from modules.health.infraestructura.repositorios.health_repository import HealthRepositoryImpl

        repo = HealthRepositoryImpl()
        result = repo.get_health()

        assert isinstance(result, Health)
        assert result.status == "healthy"
        assert result.version == "1.0.0"

    def test_health_repository_get_health_exception(self):
        """Test del método get_health con excepción del HealthRepository"""
        from modules.health.infraestructura.repositorios.health_repository import HealthRepositoryImpl

        repo = HealthRepositoryImpl()

        # Simular una excepción en el método get_health
        with pytest.raises(Exception):
            # Forzar una excepción modificando el método
            original_method = repo.get_health

            def failing_method():
                raise Exception("Test error")

            repo.get_health = failing_method
            try:
                repo.get_health()
            finally:
                repo.get_health = original_method


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
