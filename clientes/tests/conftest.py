"""
Configuración compartida para todos los tests
"""

import os
import sys

# Agregar el directorio src al path de Python para todos los tests
# Esto permite importar módulos usando 'from src.xxx import yyy'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import pytest


@pytest.fixture(scope="session")
def app():
    """Crea una aplicación Flask para los tests que requieren contexto de aplicación"""
    # Crear una app de Flask mínima para tests (sin importar Config para evitar ciclos)
    from flask import Flask

    test_app = Flask(__name__)
    test_app.config["TESTING"] = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar la base de datos en el contexto de la app
    from src.infraestructura.config.db import db_clientes, init_db_clientes

    # Importar modelos para que SQLAlchemy los registre
    from src.infraestructura.dto.cliente import ClienteModel  # noqa: F401

    with test_app.app_context():
        init_db_clientes(test_app)
        db_clientes.create_all()
        yield test_app


@pytest.fixture
def app_context(app):
    """Proporciona un contexto de aplicación para los tests"""
    with app.app_context():
        yield app
