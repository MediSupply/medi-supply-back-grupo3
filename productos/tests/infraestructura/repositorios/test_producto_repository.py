"""
Tests unitarios para ProductoRepositoryImpl
"""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

# Importar después de configurar el path para evitar importaciones circulares
from src.dominio.entities.producto import Producto

# No importar ProductoModel directamente para evitar importaciones circulares


class TestProductoRepositoryImpl:
    """Tests para ProductoRepositoryImpl"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock de la sesión de base de datos"""
        mock_session = MagicMock()
        return mock_session

    @pytest.fixture
    def sample_producto_model(self):
        """Crea un modelo de producto de ejemplo"""
        # Usar MagicMock sin spec para evitar importaciones circulares
        model = MagicMock()
        model.id = "prod-001"
        model.nombre = "Laptop"
        model.descripcion = "Laptop gaming"
        model.categoria = "electronicos"
        model.condiciones_almacenamiento = "Temperatura ambiente"
        model.valor_unitario = 1500.00
        model.cantidad_disponible = 10
        model.fecha_vencimiento = datetime(2025, 12, 31)
        model.lote = "LOT-001"
        model.tiempo_estimado_entrega = "5 días"
        model.id_proveedor = "prov-001"
        model.ubicacion = "Almacén A - Estante 3"
        return model

    def test_model_to_entity(self, sample_producto_model):
        """Test de conversión de modelo a entidad"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        repository = ProductoRepositoryImpl()
        entity = repository._model_to_entity(sample_producto_model)

        assert isinstance(entity, Producto)
        assert entity.id == "prod-001"
        assert entity.nombre == "Laptop"
        assert entity.valor_unitario == 1500.00
        assert entity.cantidad_disponible == 10

    def test_entity_to_model(self, sample_producto):
        """Test de conversión de entidad a modelo"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        repository = ProductoRepositoryImpl()
        model = repository._entity_to_model(sample_producto)

        # Verificar que el modelo tiene los atributos correctos
        assert model.id == "prod-001"
        assert model.nombre == "Laptop"
        assert model.valor_unitario == 1500.00
        assert model.cantidad_disponible == 10

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_todos_exitoso(self, mock_db, sample_producto_model):
        """Test de obtener todos los productos exitosamente"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.all.return_value = [sample_producto_model]
        mock_db.session.query.return_value = mock_query
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_todos()

        # Assert
        assert len(result) == 1
        assert result[0].id == "prod-001"
        mock_db.session.query.assert_called_once()

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_todos_vacio(self, mock_db):
        """Test de obtener todos los productos cuando no hay productos"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.all.return_value = []
        mock_db.session.query.return_value = mock_query
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_todos()

        # Assert
        assert len(result) == 0

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_todos_error(self, mock_db):
        """Test de obtener todos los productos con error"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_todos()

        # Assert
        assert len(result) == 0

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_por_id_exitoso(self, mock_db, sample_producto_model):
        """Test de obtener producto por ID exitosamente"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = sample_producto_model
        mock_db.session.query.return_value = mock_query
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_por_id("prod-001")

        # Assert
        assert result is not None
        assert result.id == "prod-001"

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_por_id_no_encontrado(self, mock_db):
        """Test de obtener producto por ID cuando no existe"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        mock_db.session.query.return_value = mock_query
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_por_id("prod-999")

        # Assert
        assert result is None

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_por_id_error(self, mock_db):
        """Test de obtener producto por ID con error"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_por_id("prod-001")

        # Assert
        assert result is None

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_por_categoria_exitoso(self, mock_db, sample_producto_model):
        """Test de obtener productos por categoría exitosamente"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.all.return_value = [sample_producto_model]
        mock_query.filter_by.return_value = mock_filter
        mock_db.session.query.return_value = mock_query
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_por_categoria("electronicos")

        # Assert
        assert len(result) == 1
        assert result[0].categoria == "electronicos"

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_obtener_por_categoria_error(self, mock_db):
        """Test de obtener productos por categoría con error"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.obtener_por_categoria("electronicos")

        # Assert
        assert len(result) == 0

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_buscar_por_nombre_exitoso(self, mock_db, sample_producto_model):
        """Test de buscar productos por nombre exitosamente"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.all.return_value = [sample_producto_model]
        mock_query.filter.return_value = mock_filter
        mock_db.session.query.return_value = mock_query
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.buscar_por_nombre("Laptop")

        # Assert
        assert len(result) == 1
        assert "Laptop" in result[0].nombre

    @patch("src.infraestructura.repositorios.producto_repository.db_productos")
    def test_buscar_por_nombre_error(self, mock_db):
        """Test de buscar productos por nombre con error"""
        from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProductoRepositoryImpl()

        # Act
        result = repository.buscar_por_nombre("Laptop")

        # Assert
        assert len(result) == 0
