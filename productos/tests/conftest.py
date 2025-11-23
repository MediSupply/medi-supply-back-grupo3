"""
Configuración compartida para todos los tests
"""
import os
import sys
from datetime import datetime
from unittest.mock import MagicMock

# Agregar el directorio src al path de Python para todos los tests
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import pytest
from flask import Flask

from src.dominio.entities.producto import Producto
from src.aplicacion.dtos.producto_dto import ProductoDto


@pytest.fixture(scope="session")
def app():
    """Crea una aplicación Flask para los tests que requieren contexto de aplicación"""
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar la base de datos en el contexto de la app
    from src.infraestructura.config.db import db_productos, init_db_productos
    
    # Importar modelos para que SQLAlchemy los registre
    from src.infraestructura.dto.producto import ProductoModel  # noqa: F401
    
    with test_app.app_context():
        init_db_productos(test_app)
        db_productos.create_all()
        yield test_app


@pytest.fixture
def app_context(app):
    """Proporciona un contexto de aplicación para los tests"""
    with app.app_context():
        yield app


@pytest.fixture
def sample_producto():
    """Crea un producto de ejemplo para los tests"""
    return Producto(
        id="prod-001",
        nombre="Laptop",
        descripcion="Laptop gaming de alta gama",
        categoria="electronicos",
        condiciones_almacenamiento="Temperatura ambiente",
        valor_unitario=1500.00,
        cantidad_disponible=10,
        fecha_vencimiento=datetime(2025, 12, 31),
        lote="LOT-001",
        tiempo_estimado_entrega="5 días",
        id_proveedor="prov-001",
    )


@pytest.fixture
def sample_producto_dto():
    """Crea un ProductoDto de ejemplo para los tests"""
    return ProductoDto(
        id="prod-001",
        nombre="Laptop",
        descripcion="Laptop gaming de alta gama",
        categoria="electronicos",
        condiciones_almacenamiento="Temperatura ambiente",
        valor_unitario=1500.00,
        cantidad_disponible=10,
        fecha_vencimiento=datetime(2025, 12, 31),
        lote="LOT-001",
        tiempo_estimado_entrega="5 días",
        id_proveedor="prov-001",
    )


@pytest.fixture
def mock_producto_repository():
    """Crea un mock del repositorio de productos"""
    mock_repo = MagicMock()
    return mock_repo

