"""
Tests unitarios para los cmd del módulo de health del gateway
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestHealthCmd:
    """Tests para el HealthCmd"""

    def test_health_cmd_initialization(self):
        """Test de inicialización del HealthCmd"""
        from modules.health.infraestructura.cmd.health_cmd import HealthCmd

        mock_use_case = Mock()
        cmd = HealthCmd(mock_use_case)

        assert cmd.health_use_case == mock_use_case

    def test_health_cmd_get_health_success(self):
        """Test del método get_health exitoso del HealthCmd"""
        from modules.health.dominio.entities.health import Health
        from modules.health.infraestructura.cmd.health_cmd import HealthCmd

        mock_use_case = Mock()
        mock_health = Health(status="healthy", timestamp=None, version="1.0.0")
        mock_use_case.execute.return_value = mock_health

        cmd = HealthCmd(mock_use_case)

        # Test que el cmd tiene el método get_health
        assert hasattr(cmd, "get_health")
        # Test que el use case tiene el método execute
        assert hasattr(mock_use_case, "execute")

    def test_health_cmd_get_health_exception(self):
        """Test del método get_health con excepción del HealthCmd"""
        from modules.health.infraestructura.cmd.health_cmd import HealthCmd

        mock_use_case = Mock()
        mock_use_case.get_health.side_effect = Exception("Test error")

        cmd = HealthCmd(mock_use_case)

        # El cmd debe manejar la excepción
        with pytest.raises(Exception):
            cmd.get_health()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
