"""
Tests unitarios para los DTOs del módulo de health del gateway
"""

import os
import sys
from datetime import datetime

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthDto:
    """Tests para el HealthDto"""

    def test_health_dto_creation(self):
        """Test de creación del HealthDto"""
        from modules.health.aplicacion.dtos.health_dto import HealthDto

        timestamp = datetime.now()
        health_dto = HealthDto(status="healthy", timestamp=timestamp, version="1.0.0")

        assert health_dto.status == "healthy"
        assert health_dto.timestamp == timestamp
        assert health_dto.version == "1.0.0"

    def test_health_dto_unhealthy(self):
        """Test de creación del HealthDto con estado unhealthy"""
        from modules.health.aplicacion.dtos.health_dto import HealthDto

        timestamp = datetime.now()
        health_dto = HealthDto(status="unhealthy", timestamp=timestamp, version="2.0.0")

        assert health_dto.status == "unhealthy"
        assert health_dto.timestamp == timestamp
        assert health_dto.version == "2.0.0"

    def test_health_dto_immutable(self):
        """Test de que HealthDto es inmutable"""
        from modules.health.aplicacion.dtos.health_dto import HealthDto

        timestamp = datetime.now()
        health_dto = HealthDto(status="healthy", timestamp=timestamp, version="1.0.0")

        # Verificar que es inmutable (no se puede modificar)
        with pytest.raises(AttributeError):
            health_dto.status = "unhealthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
