"""
Tests unitarios para ProvedorUseCase
"""

from unittest.mock import MagicMock

import pytest
from src.aplicacion.use_cases.provedor_use_case import ProvedorUseCase
from src.dominio.entities.provedor import Pais, Provedor


class TestProvedorUseCase:
    """Tests para ProvedorUseCase"""

    def test_obtener_todos_los_provedores(self):
        """Test de obtener todos los proveedores"""
        # Arrange
        mock_service = MagicMock()
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
        ]
        mock_service.obtener_todos_los_provedores.return_value = provedores
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.obtener_todos_los_provedores()

        # Assert
        assert len(result) == 1
        assert result[0].id == 1
        mock_service.obtener_todos_los_provedores.assert_called_once()

    def test_obtener_provedor_por_id_existente(self):
        """Test de obtener proveedor por ID cuando existe"""
        # Arrange
        mock_service = MagicMock()
        provedor = Provedor(
            id=1,
            nit=900123456,
            nombre="Proveedor Test",
            pais=Pais.COLOMBIA,
            direccion="Calle 123",
            telefono=6012345678,
            email="proveedor@test.com",
        )
        mock_service.obtener_provedor_por_id.return_value = provedor
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.obtener_provedor_por_id(1)

        # Assert
        assert result is not None
        assert result.id == 1
        mock_service.obtener_provedor_por_id.assert_called_once_with(1)

    def test_obtener_provedor_por_id_no_existente(self):
        """Test de obtener proveedor por ID cuando no existe"""
        # Arrange
        mock_service = MagicMock()
        mock_service.obtener_provedor_por_id.return_value = None
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.obtener_provedor_por_id(999)

        # Assert
        assert result is None
        mock_service.obtener_provedor_por_id.assert_called_once_with(999)

    def test_obtener_provedor_por_nit_existente(self):
        """Test de obtener proveedor por NIT cuando existe"""
        # Arrange
        mock_service = MagicMock()
        provedor = Provedor(
            id=1,
            nit=900123456,
            nombre="Proveedor Test",
            pais=Pais.COLOMBIA,
            direccion="Calle 123",
            telefono=6012345678,
            email="proveedor@test.com",
        )
        mock_service.obtener_provedor_por_nit.return_value = provedor
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.obtener_provedor_por_nit(900123456)

        # Assert
        assert result is not None
        assert result.nit == 900123456
        mock_service.obtener_provedor_por_nit.assert_called_once_with(900123456)

    def test_obtener_provedor_por_nit_no_existente(self):
        """Test de obtener proveedor por NIT cuando no existe"""
        # Arrange
        mock_service = MagicMock()
        mock_service.obtener_provedor_por_nit.return_value = None
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.obtener_provedor_por_nit(999999999)

        # Assert
        assert result is None
        mock_service.obtener_provedor_por_nit.assert_called_once_with(999999999)

    def test_obtener_provedores_por_pais(self):
        """Test de obtener proveedores por país"""
        # Arrange
        mock_service = MagicMock()
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
        mock_service.obtener_provedores_por_pais.return_value = provedores
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.obtener_provedores_por_pais("colombia")

        # Assert
        assert len(result) == 1
        assert result[0].pais == Pais.COLOMBIA
        mock_service.obtener_provedores_por_pais.assert_called_once_with("colombia")

    def test_buscar_provedores_por_nombre(self):
        """Test de buscar proveedores por nombre"""
        # Arrange
        mock_service = MagicMock()
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
        mock_service.buscar_provedores_por_nombre.return_value = provedores
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.buscar_provedores_por_nombre("Tecnología")

        # Assert
        assert len(result) == 1
        assert "Tecnología" in result[0].nombre
        mock_service.buscar_provedores_por_nombre.assert_called_once_with("Tecnología")

    def test_crear_provedor(self, sample_provedor):
        """Test de crear proveedor"""
        # Arrange
        mock_service = MagicMock()
        nuevo_provedor = Provedor(
            id=0,
            nit=123456789,
            nombre="Nuevo Proveedor",
            pais=Pais.COLOMBIA,
            direccion="Calle Nueva",
            telefono=6012345678,
            email="nuevo@test.com",
        )
        mock_service.crear_provedor.return_value = sample_provedor
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.crear_provedor(nuevo_provedor)

        # Assert
        assert result is not None
        mock_service.crear_provedor.assert_called_once_with(nuevo_provedor)

    def test_actualizar_provedor(self, sample_provedor):
        """Test de actualizar proveedor"""
        # Arrange
        mock_service = MagicMock()
        provedor_actualizado = Provedor(
            id=sample_provedor.id,
            nit=sample_provedor.nit,
            nombre="Nombre Actualizado",
            pais=sample_provedor.pais,
            direccion=sample_provedor.direccion,
            telefono=sample_provedor.telefono,
            email=sample_provedor.email,
        )
        mock_service.actualizar_provedor.return_value = provedor_actualizado
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.actualizar_provedor(provedor_actualizado)

        # Assert
        assert result is not None
        assert result.nombre == "Nombre Actualizado"
        mock_service.actualizar_provedor.assert_called_once_with(provedor_actualizado)

    def test_eliminar_provedor(self):
        """Test de eliminar proveedor"""
        # Arrange
        mock_service = MagicMock()
        mock_service.eliminar_provedor.return_value = True
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.eliminar_provedor(1)

        # Assert
        assert result is True
        mock_service.eliminar_provedor.assert_called_once_with(1)

    def test_eliminar_provedor_no_existente(self):
        """Test de eliminar proveedor que no existe"""
        # Arrange
        mock_service = MagicMock()
        mock_service.eliminar_provedor.return_value = False
        use_case = ProvedorUseCase(mock_service)

        # Act
        result = use_case.eliminar_provedor(999)

        # Assert
        assert result is False
        mock_service.eliminar_provedor.assert_called_once_with(999)
