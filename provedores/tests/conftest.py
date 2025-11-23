"""
Configuración compartida para todos los tests
"""

import os
import sys
from unittest.mock import MagicMock

# Agregar el directorio src al path de Python para todos los tests
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import pytest
from flask import Flask
from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto
from src.dominio.entities.provedor import Pais, Provedor


@pytest.fixture(scope="session")
def app():
    """Crea una aplicación Flask para los tests que requieren contexto de aplicación"""
    test_app = Flask(__name__)
    test_app.config["TESTING"] = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar la base de datos en el contexto de la app
    from src.infraestructura.config.db import db_provedores, init_db_provedores

    # Importar modelos para que SQLAlchemy los registre
    from src.infraestructura.dto.provedor import ProvedorModel  # noqa: F401

    with test_app.app_context():
        init_db_provedores(test_app)
        db_provedores.create_all()
        yield test_app


@pytest.fixture
def app_context(app):
    """Proporciona un contexto de aplicación para los tests"""
    with app.app_context():
        yield app


@pytest.fixture
def sample_provedor():
    """Crea un proveedor de ejemplo para los tests"""
    return Provedor(
        id=1,
        nit=900123456,
        nombre="Tecnología Avanzada S.A.S",
        pais=Pais.COLOMBIA,
        direccion="Calle 123 #45-67, Bogotá",
        telefono=6012345678,
        email="contacto@tecnologiaavanzada.com",
    )


@pytest.fixture
def sample_provedor_dto():
    """Crea un ProvedorDto de ejemplo para los tests"""
    return ProvedorDto(
        id=1,
        nit=900123456,
        nombre="Tecnología Avanzada S.A.S",
        pais=PaisDto.COLOMBIA,
        direccion="Calle 123 #45-67, Bogotá",
        telefono=6012345678,
        email="contacto@tecnologiaavanzada.com",
    )


@pytest.fixture
def mock_provedor_repository():
    """Crea un mock del repositorio de proveedores"""
    mock_repo = MagicMock()
    return mock_repo
