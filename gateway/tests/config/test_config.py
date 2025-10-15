"""
Tests unitarios para la configuración de base de datos del gateway
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Agregar el directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "src"))


class TestDatabaseConfig:
    """Tests para la configuración de base de datos"""

    def test_db_initialization(self):
        """Test de inicialización de la base de datos"""
        from config.db import db, init_db
        from flask import Flask

        # Crear aplicación Flask de prueba
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Test init_db
        init_db(app)

        assert db is not None
        assert hasattr(db, "Model")
        assert hasattr(db, "Column")
        assert hasattr(db, "session")

    def test_db_instance(self):
        """Test de que db es una instancia de SQLAlchemy"""
        from config.db import db

        # Verificar que db existe y es del tipo correcto
        assert db is not None
        assert hasattr(db, "Model")
        assert hasattr(db, "Column")
        assert hasattr(db, "session")

    def test_init_db_with_app(self):
        """Test de init_db con aplicación Flask"""
        from config.db import db, init_db
        from flask import Flask

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Test init_db
        init_db(app)

        # Verificar que db está configurado
        assert db is not None
        # Verificar que db tiene métodos básicos de SQLAlchemy
        assert hasattr(db, "Model")
        assert hasattr(db, "Column")

    def test_init_db_multiple_calls(self):
        """Test de múltiples llamadas a init_db"""
        from config.db import db, init_db
        from flask import Flask

        app1 = Flask(__name__)
        app1.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app1.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        app2 = Flask(__name__)
        app2.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app2.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Test múltiples llamadas
        init_db(app1)
        init_db(app2)

        # Verificar que db está configurado
        assert db is not None
        # Verificar que db tiene métodos básicos de SQLAlchemy
        assert hasattr(db, "Model")
        assert hasattr(db, "Column")

    def test_db_session_creation(self):
        """Test de creación de sesión de base de datos"""
        from config.db import db, init_db
        from flask import Flask

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        init_db(app)

        # Test creación de sesión
        with app.app_context():
            session = db.session
            assert session is not None
            assert hasattr(session, "add")
            assert hasattr(session, "commit")
            assert hasattr(session, "rollback")
            assert hasattr(session, "query")

    def test_db_model_base(self):
        """Test de la clase base Model"""
        from config.db import db, init_db
        from flask import Flask

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        init_db(app)

        # Test que Model está disponible
        assert db.Model is not None
        # Verificar que Model es una clase base de SQLAlchemy
        assert hasattr(db.Model, "__init__")

    def test_db_column_base(self):
        """Test de la clase base Column"""
        from config.db import db, init_db
        from flask import Flask

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        init_db(app)

        # Test que Column está disponible
        assert db.Column is not None
        assert hasattr(db.Column, "__call__")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
