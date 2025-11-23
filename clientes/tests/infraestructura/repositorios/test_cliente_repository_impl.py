"""
Tests unitarios para la implementación del repositorio de clientes
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteRepositoryImpl:
    """Tests para ClienteRepositoryImpl"""

    @pytest.fixture
    def mock_db_session(self):
        """Fixture para mock de la sesión de base de datos"""
        with patch("src.infraestructura.repositorios.cliente_repository.db_clientes") as mock_db:
            yield mock_db

    @pytest.fixture
    def cliente_repository(self, app_context):
        """Fixture para crear una instancia del repositorio"""
        from src.infraestructura.repositorios.cliente_repository import ClienteRepositoryImpl

        return ClienteRepositoryImpl()

    def test_repository_creation(self, cliente_repository):
        """Test de creación del repositorio"""
        assert cliente_repository is not None

    def test_model_to_entity_conversion(self, cliente_repository):
        """Test de conversión de modelo a entidad"""
        from src.infraestructura.dto.cliente import ClienteModel

        mock_model = MagicMock()
        mock_model.id = "cli-001"
        mock_model.nombre = "Hospital Test"
        mock_model.email = "test@test.com"
        mock_model.telefono = "+57 1 111 2222"
        mock_model.direccion = "Dirección Test"
        mock_model.razon_social = "Razón Social Test"
        mock_model.nit = "900111222-3"

        entity = cliente_repository._model_to_entity(mock_model)

        assert entity.id == "cli-001"
        assert entity.nombre == "Hospital Test"
        assert entity.email == "test@test.com"

    def test_entity_to_model_conversion(self, cliente_repository):
        """Test de conversión de entidad a modelo"""
        from src.dominio.entities.cliente import Cliente

        entity = Cliente(
            id="cli-001",
            nombre="Hospital Test",
            email="test@test.com",
            telefono="+57 1 111 2222",
            direccion="Dirección Test",
            razon_social="Razón Social Test",
            nit="900111222-3",
        )

        model = cliente_repository._entity_to_model(entity)

        assert model.id == "cli-001"
        assert model.nombre == "Hospital Test"
        assert model.email == "test@test.com"

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_obtener_todos(self, mock_db, cliente_repository):
        """Test de obtener todos los clientes"""
        from src.dominio.entities.cliente import Cliente

        # Crear mocks de modelos (sin spec para evitar problemas con SQLAlchemy)
        mock_model1 = MagicMock()
        mock_model1.id = "cli-001"
        mock_model1.nombre = "Hospital 1"
        mock_model1.email = "h1@test.com"
        mock_model1.telefono = "+57 1 111 1111"
        mock_model1.direccion = "Dirección 1"
        mock_model1.razon_social = "Razón 1"
        mock_model1.nit = "900111111-1"

        mock_model2 = MagicMock()
        mock_model2.id = "cli-002"
        mock_model2.nombre = "Hospital 2"
        mock_model2.email = "h2@test.com"
        mock_model2.telefono = "+57 1 222 2222"
        mock_model2.direccion = "Dirección 2"
        mock_model2.razon_social = "Razón 2"
        mock_model2.nit = "900222222-2"

        # Configurar el mock de la sesión
        mock_db.session.query.return_value.all.return_value = [mock_model1, mock_model2]

        clientes = cliente_repository.obtener_todos()

        assert len(clientes) == 2
        assert all(isinstance(c, Cliente) for c in clientes)
        assert clientes[0].id == "cli-001"
        assert clientes[1].id == "cli-002"

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_obtener_todos_con_error(self, mock_db, cliente_repository):
        """Test de obtener todos los clientes cuando hay un error"""
        mock_db.session.query.return_value.all.side_effect = Exception("Error de conexión")

        clientes = cliente_repository.obtener_todos()

        assert isinstance(clientes, list)
        assert len(clientes) == 0

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_obtener_por_id_encontrado(self, mock_db, cliente_repository):
        """Test de obtener cliente por ID cuando existe"""
        from src.dominio.entities.cliente import Cliente

        mock_model = MagicMock()
        mock_model.id = "cli-001"
        mock_model.nombre = "Hospital Test"
        mock_model.email = "test@test.com"
        mock_model.telefono = "+57 1 333 3333"
        mock_model.direccion = "Dirección Test"
        mock_model.razon_social = "Razón Test"
        mock_model.nit = "900333333-3"

        mock_db.session.query.return_value.filter_by.return_value.first.return_value = mock_model

        cliente = cliente_repository.obtener_por_id("cli-001")

        assert cliente is not None
        assert isinstance(cliente, Cliente)
        assert cliente.id == "cli-001"
        assert cliente.nombre == "Hospital Test"

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_obtener_por_id_no_encontrado(self, mock_db, cliente_repository):
        """Test de obtener cliente por ID cuando no existe"""
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = None

        cliente = cliente_repository.obtener_por_id("cli-inexistente")

        assert cliente is None

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_obtener_por_id_con_error(self, mock_db, cliente_repository):
        """Test de obtener cliente por ID cuando hay un error"""
        mock_db.session.query.return_value.filter_by.return_value.first.side_effect = Exception("Error de conexión")

        cliente = cliente_repository.obtener_por_id("cli-001")

        assert cliente is None

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_buscar_por_nombre(self, mock_db, cliente_repository):
        """Test de búsqueda por nombre"""
        from src.dominio.entities.cliente import Cliente

        mock_model = MagicMock()
        mock_model.id = "cli-001"
        mock_model.nombre = "Hospital Central"
        mock_model.email = "central@test.com"
        mock_model.telefono = "+57 1 444 4444"
        mock_model.direccion = "Dirección Central"
        mock_model.razon_social = "Razón Central"
        mock_model.nit = "900444444-4"

        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = [mock_model]
        mock_db.session.query.return_value = mock_query

        clientes = cliente_repository.buscar_por_nombre("Central")

        assert len(clientes) == 1
        assert isinstance(clientes[0], Cliente)
        assert "Central" in clientes[0].nombre

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_buscar_por_nombre_con_error(self, mock_db, cliente_repository):
        """Test de búsqueda por nombre cuando hay un error"""
        mock_query = MagicMock()
        mock_query.filter.return_value.all.side_effect = Exception("Error de conexión")
        mock_db.session.query.return_value = mock_query

        clientes = cliente_repository.buscar_por_nombre("Test")

        assert isinstance(clientes, list)
        assert len(clientes) == 0

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_crear_cliente(self, mock_db, cliente_repository):
        """Test de crear cliente"""
        from src.dominio.entities.cliente import Cliente

        nuevo_cliente = Cliente(
            id="cli-new",
            nombre="Hospital Nuevo",
            email="nuevo@test.com",
            telefono="+57 1 555 5555",
            direccion="Dirección Nueva",
            razon_social="Razón Nueva",
            nit="900555555-5",
        )

        # Mock del modelo que se creará
        mock_model = MagicMock()
        mock_model.id = "cli-new"
        mock_model.nombre = "Hospital Nuevo"
        mock_model.email = "nuevo@test.com"
        mock_model.telefono = "+57 1 555 5555"
        mock_model.direccion = "Dirección Nueva"
        mock_model.razon_social = "Razón Nueva"
        mock_model.nit = "900555555-5"

        # Configurar el mock para la verificación de NIT duplicado (no existe)
        mock_query_nit = MagicMock()
        mock_query_nit.filter_by.return_value.first.return_value = None

        # Configurar mock_db.session.query para que retorne el query mock
        # Primera llamada: verificación de NIT
        # Segunda llamada: después de crear, para convertir a entidad (no se usa realmente)
        mock_db.session.query.return_value = mock_query_nit

        # Crear el cliente
        cliente_creado = cliente_repository.crear(nuevo_cliente)

        assert cliente_creado is not None
        assert isinstance(cliente_creado, Cliente)
        assert cliente_creado.id == "cli-new"
        assert cliente_creado.nombre == "Hospital Nuevo"
        # Verificar que se llamó a db_clientes.session.add (con el modelo creado)
        mock_db.session.add.assert_called_once()
        # Verificar que se llamó a db_clientes.session.commit
        mock_db.session.commit.assert_called_once()

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_crear_cliente_nit_duplicado(self, mock_db, cliente_repository):
        """Test de crear cliente con NIT duplicado"""
        from src.dominio.entities.cliente import Cliente

        nuevo_cliente = Cliente(
            id="cli-new",
            nombre="Hospital Nuevo",
            email="nuevo@test.com",
            telefono="+57 1 555 5555",
            direccion="Dirección Nueva",
            razon_social="Razón Nueva",
            nit="900555555-5",
        )

        # Mock para simular que ya existe un cliente con ese NIT
        mock_existing = MagicMock()
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_existing
        mock_db.session.query.return_value = mock_query

        with pytest.raises(ValueError, match="Ya existe un cliente con el NIT"):
            cliente_repository.crear(nuevo_cliente)

        # Verificar que no se hizo commit
        mock_db.session.commit.assert_not_called()
        # Verificar que se hizo rollback
        mock_db.session.rollback.assert_called_once()

    @patch("src.infraestructura.repositorios.cliente_repository.db_clientes")
    def test_crear_cliente_con_error_generico(self, mock_db, cliente_repository):
        """Test de crear cliente cuando hay un error genérico"""
        from src.dominio.entities.cliente import Cliente

        nuevo_cliente = Cliente(
            id="cli-new",
            nombre="Hospital Nuevo",
            email="nuevo@test.com",
            telefono="+57 1 555 5555",
            direccion="Dirección Nueva",
            razon_social="Razón Nueva",
            nit="900555555-5",
        )

        # Configurar para que no haya NIT duplicado pero luego falle el commit
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None  # No existe
        mock_db.session.query.return_value = mock_query
        mock_db.session.commit.side_effect = Exception("Error de base de datos")

        with pytest.raises(Exception):
            cliente_repository.crear(nuevo_cliente)

        # Verificar que se hizo rollback
        mock_db.session.rollback.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
