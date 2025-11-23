"""
Tests unitarios para ProvedorService
"""

from unittest.mock import MagicMock
import pytest

from src.aplicacion.servicios.provedor_service import ProvedorService
from src.dominio.entities.provedor import Pais, Provedor


class TestProvedorService:
    """Tests para ProvedorService"""

    def test_obtener_todos_los_provedores(self, mock_provedor_repository):
        """Test de obtener todos los proveedores"""
        # Arrange
        provedores = [
            Provedor(
                id=1,
                nit=900123456,
                nombre="Proveedor 1",
                pais=Pais.COLOMBIA,
                direccion="Calle 123",
                telefono=6012345678,
                email="proveedor1@test.com",
            ),
            Provedor(
                id=2,
                nit=800987654,
                nombre="Proveedor 2",
                pais=Pais.MEXICO,
                direccion="Av. Principal 456",
                telefono=5551234567,
                email="proveedor2@test.com",
            ),
        ]
        mock_provedor_repository.obtener_todos.return_value = provedores
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.obtener_todos_los_provedores()

        # Assert
        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        mock_provedor_repository.obtener_todos.assert_called_once()

    def test_obtener_provedor_por_id_existente(self, mock_provedor_repository):
        """Test de obtener proveedor por ID cuando existe"""
        # Arrange
        provedor = Provedor(
            id=1,
            nit=900123456,
            nombre="Proveedor Test",
            pais=Pais.COLOMBIA,
            direccion="Calle 123",
            telefono=6012345678,
            email="proveedor@test.com",
        )
        mock_provedor_repository.obtener_por_id.return_value = provedor
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.obtener_provedor_por_id(1)

        # Assert
        assert result is not None
        assert result.id == 1
        assert result.nombre == "Proveedor Test"
        mock_provedor_repository.obtener_por_id.assert_called_once_with(1)

    def test_obtener_provedor_por_id_no_existente(self, mock_provedor_repository):
        """Test de obtener proveedor por ID cuando no existe"""
        # Arrange
        mock_provedor_repository.obtener_por_id.return_value = None
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.obtener_provedor_por_id(999)

        # Assert
        assert result is None
        mock_provedor_repository.obtener_por_id.assert_called_once_with(999)

    def test_obtener_provedor_por_nit_existente(self, mock_provedor_repository):
        """Test de obtener proveedor por NIT cuando existe"""
        # Arrange
        provedor = Provedor(
            id=1,
            nit=900123456,
            nombre="Proveedor Test",
            pais=Pais.COLOMBIA,
            direccion="Calle 123",
            telefono=6012345678,
            email="proveedor@test.com",
        )
        mock_provedor_repository.obtener_por_nit.return_value = provedor
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.obtener_provedor_por_nit(900123456)

        # Assert
        assert result is not None
        assert result.nit == 900123456
        mock_provedor_repository.obtener_por_nit.assert_called_once_with(900123456)

    def test_obtener_provedor_por_nit_no_existente(self, mock_provedor_repository):
        """Test de obtener proveedor por NIT cuando no existe"""
        # Arrange
        mock_provedor_repository.obtener_por_nit.return_value = None
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.obtener_provedor_por_nit(999999999)

        # Assert
        assert result is None
        mock_provedor_repository.obtener_por_nit.assert_called_once_with(999999999)

    def test_obtener_provedores_por_pais(self, mock_provedor_repository):
        """Test de obtener proveedores por país"""
        # Arrange
        provedores = [
            Provedor(
                id=1,
                nit=900123456,
                nombre="Proveedor Colombia",
                pais=Pais.COLOMBIA,
                direccion="Bogotá",
                telefono=6012345678,
                email="colombia@test.com",
            ),
        ]
        mock_provedor_repository.obtener_por_pais.return_value = provedores
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.obtener_provedores_por_pais("colombia")

        # Assert
        assert len(result) == 1
        assert result[0].pais == Pais.COLOMBIA
        mock_provedor_repository.obtener_por_pais.assert_called_once_with("colombia")

    def test_buscar_provedores_por_nombre(self, mock_provedor_repository):
        """Test de buscar proveedores por nombre"""
        # Arrange
        provedores = [
            Provedor(
                id=1,
                nit=900123456,
                nombre="Tecnología Avanzada",
                pais=Pais.COLOMBIA,
                direccion="Bogotá",
                telefono=6012345678,
                email="tecnologia@test.com",
            ),
        ]
        mock_provedor_repository.buscar_por_nombre.return_value = provedores
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.buscar_provedores_por_nombre("Tecnología")

        # Assert
        assert len(result) == 1
        assert "Tecnología" in result[0].nombre
        mock_provedor_repository.buscar_por_nombre.assert_called_once_with("Tecnología")

    def test_buscar_provedores_por_nombre_sin_resultados(self, mock_provedor_repository):
        """Test de buscar proveedores por nombre sin resultados"""
        # Arrange
        mock_provedor_repository.buscar_por_nombre.return_value = []
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.buscar_provedores_por_nombre("Inexistente")

        # Assert
        assert len(result) == 0
        mock_provedor_repository.buscar_por_nombre.assert_called_once_with("Inexistente")

    def test_crear_provedor(self, mock_provedor_repository, sample_provedor):
        """Test de crear proveedor"""
        # Arrange
        nuevo_provedor = Provedor(
            id=0,
            nit=123456789,
            nombre="Nuevo Proveedor",
            pais=Pais.COLOMBIA,
            direccion="Calle Nueva",
            telefono=6012345678,
            email="nuevo@test.com",
        )
        mock_provedor_repository.crear.return_value = sample_provedor
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.crear_provedor(nuevo_provedor)

        # Assert
        assert result is not None
        mock_provedor_repository.crear.assert_called_once_with(nuevo_provedor)

    def test_actualizar_provedor(self, mock_provedor_repository, sample_provedor):
        """Test de actualizar proveedor"""
        # Arrange
        provedor_actualizado = Provedor(
            id=sample_provedor.id,
            nit=sample_provedor.nit,
            nombre="Nombre Actualizado",
            pais=sample_provedor.pais,
            direccion=sample_provedor.direccion,
            telefono=sample_provedor.telefono,
            email=sample_provedor.email,
        )
        mock_provedor_repository.actualizar.return_value = provedor_actualizado
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.actualizar_provedor(provedor_actualizado)

        # Assert
        assert result is not None
        assert result.nombre == "Nombre Actualizado"
        mock_provedor_repository.actualizar.assert_called_once_with(provedor_actualizado)

    def test_eliminar_provedor(self, mock_provedor_repository):
        """Test de eliminar proveedor"""
        # Arrange
        mock_provedor_repository.eliminar.return_value = True
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.eliminar_provedor(1)

        # Assert
        assert result is True
        mock_provedor_repository.eliminar.assert_called_once_with(1)

    def test_eliminar_provedor_no_existente(self, mock_provedor_repository):
        """Test de eliminar proveedor que no existe"""
        # Arrange
        mock_provedor_repository.eliminar.return_value = False
        service = ProvedorService(mock_provedor_repository)

        # Act
        result = service.eliminar_provedor(999)

        # Assert
        assert result is False
        mock_provedor_repository.eliminar.assert_called_once_with(999)

