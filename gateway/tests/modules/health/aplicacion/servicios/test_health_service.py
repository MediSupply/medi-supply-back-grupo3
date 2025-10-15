"""
Tests unitarios para el servicio de health del gateway
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthService:
    """Tests para el servicio de health"""

    def test_health_service_initialization(self):
        """Test de inicialización del HealthService"""
        from modules.health.aplicacion.servicios.health_service import HealthService

        mock_repo = Mock()
        service = HealthService(mock_repo)

        assert service.health_repository == mock_repo

    def test_health_service_get_health_success(self):
        """Test del método get_health exitoso"""
        from modules.health.aplicacion.servicios.health_service import HealthService
        from modules.health.dominio.entities.health import Health

        mock_repo = Mock()
        service = HealthService(mock_repo)

        # Test get_health sin excepciones
        result = service.get_health()

        assert result is not None
        assert result.status == "healthy"
        assert result.version == "1.0.0"
        assert result.timestamp is not None

    @patch("modules.health.aplicacion.servicios.health_service.Health")
    def test_health_service_get_health_exception(self, mock_health_class):
        """Test del método get_health con excepción"""
        from modules.health.aplicacion.servicios.health_service import HealthService

        mock_repo = Mock()
        service = HealthService(mock_repo)

        # Mock Health.healthy para que lance excepción
        mock_health_class.healthy.side_effect = Exception("Test error")

        # Mock Health.unhealthy para que devuelva un objeto con status "unhealthy"
        mock_unhealthy = Mock()
        mock_unhealthy.status = "unhealthy"
        mock_unhealthy.version = "1.0.0"
        mock_unhealthy.timestamp = Mock()
        mock_health_class.unhealthy.return_value = mock_unhealthy

        # Test get_health con excepción
        result = service.get_health()

        # El servicio debe manejar la excepción y devolver unhealthy
        assert result is not None
        assert result.status == "unhealthy"

    def test_health_service_get_health_custom_version(self):
        """Test del método get_health - el servicio usa versión por defecto"""
        from modules.health.aplicacion.servicios.health_service import HealthService

        mock_repo = Mock()
        service = HealthService(mock_repo)

        # Test get_health - el servicio no acepta parámetros de versión
        result = service.get_health()

        assert result is not None
        assert result.status == "healthy"
        assert result.version == "1.0.0"  # Versión por defecto
        assert result.timestamp is not None

    @patch("modules.health.aplicacion.servicios.health_service.Health")
    def test_health_service_get_health_exception_with_version(self, mock_health_class):
        """Test del método get_health con excepción - el servicio usa versión por defecto"""
        from modules.health.aplicacion.servicios.health_service import HealthService

        mock_repo = Mock()
        service = HealthService(mock_repo)

        # Mock Health.healthy para que lance excepción
        mock_health_class.healthy.side_effect = Exception("Test error")

        # Mock Health.unhealthy para que devuelva un objeto con status "unhealthy"
        mock_unhealthy = Mock()
        mock_unhealthy.status = "unhealthy"
        mock_unhealthy.version = "1.0.0"
        mock_unhealthy.timestamp = Mock()
        mock_health_class.unhealthy.return_value = mock_unhealthy

        # Test get_health con excepción - el servicio no acepta parámetros de versión
        result = service.get_health()

        # El servicio debe manejar la excepción y devolver unhealthy
        assert result is not None
        assert result.status == "unhealthy"

    def test_health_service_repository_not_used(self):
        """Test de que el servicio no usa el repositorio (health check simple)"""
        from modules.health.aplicacion.servicios.health_service import HealthService

        mock_repo = Mock()
        service = HealthService(mock_repo)

        # Ejecutar get_health
        result = service.get_health()

        # Verificar que el repositorio no fue llamado
        mock_repo.assert_not_called()

        # Verificar que el resultado es válido
        assert result is not None
        assert result.status == "healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
