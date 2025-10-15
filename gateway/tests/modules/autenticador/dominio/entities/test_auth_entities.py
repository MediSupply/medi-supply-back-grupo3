"""
Tests unitarios para las entidades del módulo de autenticación del gateway
"""

import os
import sys
from datetime import datetime, timedelta

import pytest

# Agregar el directorio src del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestUserEntity:
    """Tests para la entidad User"""

    def test_user_entity_creation(self):
        """Test de creación de la entidad User"""
        # Importar directamente sin pasar por __init__.py
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "user",
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "..",
                "src",
                "modules",
                "autenticador",
                "dominio",
                "entities",
                "user.py",
            ),
        )
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        User = user_module.User
        Role = user_module.Role

        user = User(id="test-id", name="Test User", email="test@example.com", password="password123", role=Role.USER)

        assert user.id == "test-id"
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.role == Role.USER

    def test_user_entity_to_dict(self):
        """Test del método to_dict de User"""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "user",
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "..",
                "src",
                "modules",
                "autenticador",
                "dominio",
                "entities",
                "user.py",
            ),
        )
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        User = user_module.User
        Role = user_module.Role

        user = User(id="test-id", name="Test User", email="test@example.com", password="password123", role=Role.USER)

        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)
        assert user_dict["id"] == "test-id"
        assert user_dict["name"] == "Test User"
        assert user_dict["email"] == "test@example.com"
        assert user_dict["password"] == "password123"
        assert user_dict["role"] == "USER"

    def test_user_entity_admin_role(self):
        """Test de creación de usuario con rol ADMIN"""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "user",
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "..",
                "src",
                "modules",
                "autenticador",
                "dominio",
                "entities",
                "user.py",
            ),
        )
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        User = user_module.User
        Role = user_module.Role

        user = User(id="admin-id", name="Admin User", email="admin@example.com", password="admin123", role=Role.ADMIN)

        assert user.role == Role.ADMIN
        assert user.to_dict()["role"] == "ADMIN"

    def test_user_entity_role_enum(self):
        """Test de los valores del enum Role"""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "user",
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "..",
                "src",
                "modules",
                "autenticador",
                "dominio",
                "entities",
                "user.py",
            ),
        )
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        Role = user_module.Role

        assert Role.USER.value == "USER"
        assert Role.ADMIN.value == "ADMIN"


class TestSessionEntity:
    """Tests para la entidad Session"""

    def test_session_entity_creation(self):
        """Test de creación de la entidad Session"""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "session",
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "..",
                "src",
                "modules",
                "autenticador",
                "dominio",
                "entities",
                "session.py",
            ),
        )
        session_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(session_module)

        Session = session_module.Session

        expires_at = datetime.now() + timedelta(hours=1)
        session = Session(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at)

        assert session.id == "session-id"
        assert session.user_id == "user-id"
        assert session.token == "jwt-token"
        assert session.expires_at == expires_at

    def test_session_entity_to_dict(self):
        """Test del método to_dict de Session"""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "session",
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "..",
                "src",
                "modules",
                "autenticador",
                "dominio",
                "entities",
                "session.py",
            ),
        )
        session_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(session_module)

        Session = session_module.Session

        expires_at = datetime.now() + timedelta(hours=1)
        session = Session(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at)

        session_dict = session.to_dict()
        assert isinstance(session_dict, dict)
        assert session_dict["id"] == "session-id"
        assert session_dict["user_id"] == "user-id"
        assert session_dict["token"] == "jwt-token"
        assert session_dict["expires_at"] == expires_at

    def test_session_entity_immutable(self):
        """Test de que Session es inmutable (frozen dataclass)"""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "session",
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "..",
                "src",
                "modules",
                "autenticador",
                "dominio",
                "entities",
                "session.py",
            ),
        )
        session_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(session_module)

        Session = session_module.Session

        expires_at = datetime.now() + timedelta(hours=1)
        session = Session(id="session-id", user_id="user-id", token="jwt-token", expires_at=expires_at)

        # Verificar que es inmutable
        with pytest.raises(AttributeError):
            session.id = "new-id"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
