"""
Tests unitarios para ProvedorRepositoryImpl
"""

from unittest.mock import MagicMock, patch

import pytest

# Importar después de configurar el path para evitar importaciones circulares
from src.dominio.entities.provedor import Pais, Provedor


class TestProvedorRepositoryImpl:
    """Tests para ProvedorRepositoryImpl"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock de la sesión de base de datos"""
        mock_session = MagicMock()
        return mock_session

    @pytest.fixture
    def sample_provedor_model(self):
        """Crea un modelo de proveedor de ejemplo"""
        # Usar MagicMock sin spec para evitar importaciones circulares
        model = MagicMock()
        model.id = 1
        model.nit = 900123456
        model.nombre = "Tecnología Avanzada S.A.S"
        model.pais = "colombia"
        model.direccion = "Calle 123 #45-67, Bogotá"
        model.telefono = 6012345678
        model.email = "contacto@tecnologiaavanzada.com"
        return model

    def test_model_to_entity(self, sample_provedor_model):
        """Test de conversión de modelo a entidad"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        repository = ProvedorRepositoryImpl()
        entity = repository._model_to_entity(sample_provedor_model)

        assert isinstance(entity, Provedor)
        assert entity.id == 1
        assert entity.nit == 900123456
        assert entity.nombre == "Tecnología Avanzada S.A.S"
        assert entity.pais == Pais.COLOMBIA

    def test_entity_to_model(self, sample_provedor):
        """Test de conversión de entidad a modelo"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        repository = ProvedorRepositoryImpl()
        model = repository._entity_to_model(sample_provedor)

        # Verificar que el modelo tiene los atributos correctos
        assert model.nit == 900123456
        assert model.nombre == "Tecnología Avanzada S.A.S"
        assert model.pais == "colombia"
        assert model.email == "contacto@tecnologiaavanzada.com"

    def test_entity_to_model_sin_id(self, sample_provedor):
        """Test de conversión de entidad a modelo sin ID (para crear)"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        repository = ProvedorRepositoryImpl()
        # Crear un proveedor sin ID
        provedor_sin_id = Provedor(
            id=0,
            nit=900123456,
            nombre="Nuevo Proveedor",
            pais=Pais.COLOMBIA,
            direccion="Calle Nueva",
            telefono=6012345678,
            email="nuevo@test.com",
        )
        model = repository._entity_to_model(provedor_sin_id, include_id=False)

        # Verificar que no tiene ID
        assert not hasattr(model, "id") or model.id is None

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_todos_exitoso(self, mock_db, sample_provedor_model):
        """Test de obtener todos los proveedores exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.all.return_value = [sample_provedor_model]
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_todos()

        # Assert
        assert len(result) == 1
        assert result[0].id == 1
        mock_db.session.query.assert_called_once()

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_todos_vacio(self, mock_db):
        """Test de obtener todos los proveedores cuando no hay proveedores"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.all.return_value = []
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_todos()

        # Assert
        assert len(result) == 0

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_todos_error(self, mock_db):
        """Test de obtener todos los proveedores con error"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_todos()

        # Assert
        assert len(result) == 0

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_por_id_exitoso(self, mock_db, sample_provedor_model):
        """Test de obtener proveedor por ID exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = sample_provedor_model
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_por_id(1)

        # Assert
        assert result is not None
        assert result.id == 1

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_por_id_no_encontrado(self, mock_db):
        """Test de obtener proveedor por ID cuando no existe"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_por_id(999)

        # Assert
        assert result is None

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_por_id_error(self, mock_db):
        """Test de obtener proveedor por ID con error"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_por_id(1)

        # Assert
        assert result is None

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_por_nit_exitoso(self, mock_db, sample_provedor_model):
        """Test de obtener proveedor por NIT exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = sample_provedor_model
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_por_nit(900123456)

        # Assert
        assert result is not None
        assert result.nit == 900123456

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_por_nit_no_encontrado(self, mock_db):
        """Test de obtener proveedor por NIT cuando no existe"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_por_nit(999999999)

        # Assert
        assert result is None

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_por_pais_exitoso(self, mock_db, sample_provedor_model):
        """Test de obtener proveedores por país exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.all.return_value = [sample_provedor_model]
        mock_query.filter_by.return_value = mock_filter
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_por_pais("colombia")

        # Assert
        assert len(result) == 1
        assert result[0].pais == Pais.COLOMBIA

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_obtener_por_pais_error(self, mock_db):
        """Test de obtener proveedores por país con error"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.obtener_por_pais("colombia")

        # Assert
        assert len(result) == 0

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_buscar_por_nombre_exitoso(self, mock_db, sample_provedor_model):
        """Test de buscar proveedores por nombre exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.all.return_value = [sample_provedor_model]
        mock_query.filter.return_value = mock_filter
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.buscar_por_nombre("Tecnología")

        # Assert
        assert len(result) == 1
        assert "Tecnología" in result[0].nombre

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_buscar_por_nombre_error(self, mock_db):
        """Test de buscar proveedores por nombre con error"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_db.session.query.side_effect = Exception("Error de base de datos")
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.buscar_por_nombre("Tecnología")

        # Assert
        assert len(result) == 0

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_crear_exitoso(self, mock_db, sample_provedor):
        """Test de crear proveedor exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_model = MagicMock()
        mock_model.id = 1
        mock_model.nit = sample_provedor.nit
        mock_model.nombre = sample_provedor.nombre
        mock_model.pais = sample_provedor.pais.value
        mock_model.direccion = sample_provedor.direccion
        mock_model.telefono = sample_provedor.telefono
        mock_model.email = sample_provedor.email

        mock_db.session.add = MagicMock()
        mock_db.session.commit = MagicMock()
        mock_db.session.refresh = MagicMock()

        repository = ProvedorRepositoryImpl()
        # Mock del método _entity_to_model para devolver el mock_model
        repository._entity_to_model = MagicMock(return_value=mock_model)
        repository._model_to_entity = MagicMock(return_value=sample_provedor)

        # Act
        result = repository.crear(sample_provedor)

        # Assert
        assert result is not None
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_crear_error(self, mock_db, sample_provedor):
        """Test de crear proveedor con error"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_db.session.add.side_effect = Exception("Error de base de datos")
        repository = ProvedorRepositoryImpl()
        repository._entity_to_model = MagicMock(return_value=MagicMock())

        # Act & Assert
        with pytest.raises(Exception):
            repository.crear(sample_provedor)
        mock_db.session.rollback.assert_called_once()

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_actualizar_exitoso(self, mock_db, sample_provedor):
        """Test de actualizar proveedor exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_model = MagicMock()
        mock_model.id = sample_provedor.id
        mock_model.nit = sample_provedor.nit
        mock_model.nombre = sample_provedor.nombre
        mock_model.pais = sample_provedor.pais.value
        mock_model.direccion = sample_provedor.direccion
        mock_model.telefono = sample_provedor.telefono
        mock_model.email = sample_provedor.email

        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_model
        mock_db.session.query.return_value = mock_query
        mock_db.session.commit = MagicMock()
        mock_db.session.refresh = MagicMock()

        repository = ProvedorRepositoryImpl()
        repository._model_to_entity = MagicMock(return_value=sample_provedor)

        # Act
        result = repository.actualizar(sample_provedor)

        # Assert
        assert result is not None
        mock_db.session.commit.assert_called_once()

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_actualizar_no_encontrado(self, mock_db, sample_provedor):
        """Test de actualizar proveedor cuando no existe"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act & Assert
        with pytest.raises(ValueError):
            repository.actualizar(sample_provedor)

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_eliminar_exitoso(self, mock_db):
        """Test de eliminar proveedor exitosamente"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_model = MagicMock()
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_model
        mock_db.session.query.return_value = mock_query
        mock_db.session.delete = MagicMock()
        mock_db.session.commit = MagicMock()
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.eliminar(1)

        # Assert
        assert result is True
        mock_db.session.delete.assert_called_once_with(mock_model)
        mock_db.session.commit.assert_called_once()

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_eliminar_no_encontrado(self, mock_db):
        """Test de eliminar proveedor cuando no existe"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        mock_db.session.query.return_value = mock_query
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.eliminar(999)

        # Assert
        assert result is False

    @patch("src.infraestructura.repositorios.provedor_repository.db_provedores")
    def test_eliminar_error(self, mock_db):
        """Test de eliminar proveedor con error"""
        from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl

        # Arrange
        mock_query = MagicMock()
        mock_model = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_model
        mock_db.session.query.return_value = mock_query
        mock_db.session.delete.side_effect = Exception("Error de base de datos")
        repository = ProvedorRepositoryImpl()

        # Act
        result = repository.eliminar(1)

        # Assert
        assert result is False
        mock_db.session.rollback.assert_called_once()
