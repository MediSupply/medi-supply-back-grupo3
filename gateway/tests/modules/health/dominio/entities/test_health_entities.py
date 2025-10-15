"""
Tests unitarios para las entidades del módulo de health del gateway
"""

import os
import sys
from datetime import datetime

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthEntity:
    """Tests para la entidad Health"""

    def test_health_entity_creation(self):
        """Test de creación de la entidad Health"""
        from modules.health.dominio.entities.health import Health

        timestamp = datetime.now()
        health = Health(status="healthy", timestamp=timestamp, version="1.0.0")

        assert health.status == "healthy"
        assert health.timestamp == timestamp
        assert health.version == "1.0.0"

    def test_health_entity_to_dict(self):
        """Test del método to_dict de Health"""
        from modules.health.dominio.entities.health import Health

        health = Health(status="healthy", timestamp=datetime.now(), version="1.0.0")

        health_dict = health.to_dict()
        assert isinstance(health_dict, dict)
        assert health_dict["status"] == "healthy"
        assert health_dict["version"] == "1.0.0"
        assert "timestamp" in health_dict

    def test_health_healthy_factory(self):
        """Test del factory method healthy"""
        from modules.health.dominio.entities.health import Health

        health = Health.healthy("2.0.0")

        assert health.status == "healthy"
        assert health.version == "2.0.0"
        assert health.timestamp is not None
        assert isinstance(health.timestamp, datetime)

    def test_health_unhealthy_factory(self):
        """Test del factory method unhealthy"""
        from modules.health.dominio.entities.health import Health

        health = Health.unhealthy("2.0.0")

        assert health.status == "unhealthy"
        assert health.version == "2.0.0"
        assert health.timestamp is not None
        assert isinstance(health.timestamp, datetime)

    def test_health_default_version(self):
        """Test de factory methods con versión por defecto"""
        from modules.health.dominio.entities.health import Health

        healthy = Health.healthy()
        unhealthy = Health.unhealthy()

        assert healthy.version == "1.0.0"
        assert unhealthy.version == "1.0.0"

    def test_health_immutable(self):
        """Test de que Health es inmutable"""
        from modules.health.dominio.entities.health import Health

        health = Health(status="healthy", timestamp=datetime.now(), version="1.0.0")

        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            health.status = "unhealthy"

    def test_health_different_statuses(self):
        """Test de diferentes estados de health"""
        from modules.health.dominio.entities.health import Health

        # Test estado healthy
        healthy = Health(status="healthy", timestamp=datetime.now(), version="1.0.0")
        assert healthy.status == "healthy"

        # Test estado unhealthy
        unhealthy = Health(status="unhealthy", timestamp=datetime.now(), version="1.0.0")
        assert unhealthy.status == "unhealthy"

        # Test estado custom
        custom = Health(status="maintenance", timestamp=datetime.now(), version="1.0.0")
        assert custom.status == "maintenance"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
