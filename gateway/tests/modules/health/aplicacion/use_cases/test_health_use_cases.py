"""
Tests unitarios para los use cases del módulo de health del gateway
"""

import os
import sys
from unittest.mock import Mock

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthUseCase:
    """Tests para el HealthUseCase"""

    def test_health_use_case_initialization(self):
        """Test de inicialización del HealthUseCase"""
        from modules.health.aplicacion.use_cases.health_use_case import HealthUseCase

        mock_service = Mock()
        use_case = HealthUseCase(mock_service)

        assert use_case.health_service == mock_service

    def test_health_use_case_get_health(self):
        """Test del método execute del HealthUseCase"""
        from modules.health.aplicacion.use_cases.health_use_case import HealthUseCase
        from modules.health.dominio.entities.health import Health

        mock_service = Mock()
        mock_health = Health(status="healthy", timestamp=None, version="1.0.0")
        mock_service.get_health.return_value = mock_health

        use_case = HealthUseCase(mock_service)
        result = use_case.execute()

        assert result == mock_health
        mock_service.get_health.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
