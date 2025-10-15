"""
Tests unitarios para los mappers del módulo de health del gateway
"""

import os
import sys
from datetime import datetime

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthMapper:
    """Tests para el HealthMapper"""

    def test_health_mapper_entity_to_dto(self):
        """Test del método entity_to_dto del HealthMapper"""
        from modules.health.aplicacion.dtos.health_dto import HealthDto
        from modules.health.aplicacion.mappers.health_mapper import HealthMapper
        from modules.health.dominio.entities.health import Health

        timestamp = datetime.now()
        health = Health(status="healthy", timestamp=timestamp, version="1.0.0")

        health_dto = HealthMapper.entity_to_dto(health)
        assert isinstance(health_dto, HealthDto)
        assert health_dto.status == "healthy"
        assert health_dto.timestamp == timestamp
        assert health_dto.version == "1.0.0"

    def test_health_mapper_dto_to_entity(self):
        """Test del método dto_to_entity del HealthMapper"""
        from modules.health.aplicacion.dtos.health_dto import HealthDto
        from modules.health.aplicacion.mappers.health_mapper import HealthMapper
        from modules.health.dominio.entities.health import Health

        timestamp = datetime.now()
        health_dto = HealthDto(status="unhealthy", timestamp=timestamp, version="2.0.0")

        health = HealthMapper.dto_to_entity(health_dto)
        assert isinstance(health, Health)
        assert health.status == "unhealthy"
        assert health.timestamp == timestamp
        assert health.version == "2.0.0"

    def test_health_mapper_dto_to_json(self):
        """Test del método dto_to_json del HealthMapper"""
        from modules.health.aplicacion.dtos.health_dto import HealthDto
        from modules.health.aplicacion.mappers.health_mapper import HealthMapper

        timestamp = datetime.now()
        health_dto = HealthDto(status="healthy", timestamp=timestamp, version="1.0.0")

        json_data = HealthMapper.dto_to_json(health_dto)
        assert isinstance(json_data, dict)
        assert json_data["status"] == "healthy"
        assert json_data["timestamp"] == timestamp.isoformat()  # Se convierte a string ISO
        assert json_data["version"] == "1.0.0"

    def test_health_mapper_json_to_dto(self):
        """Test del método json_to_dto del HealthMapper"""
        from modules.health.aplicacion.dtos.health_dto import HealthDto
        from modules.health.aplicacion.mappers.health_mapper import HealthMapper

        timestamp = datetime.now()
        json_data = {
            "status": "unhealthy",
            "timestamp": timestamp.isoformat(),
            "version": "2.0.0",
        }  # timestamp como string ISO

        health_dto = HealthMapper.json_to_dto(json_data)
        assert isinstance(health_dto, HealthDto)
        assert health_dto.status == "unhealthy"
        assert health_dto.timestamp == timestamp  # Se convierte de vuelta a datetime
        assert health_dto.version == "2.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
