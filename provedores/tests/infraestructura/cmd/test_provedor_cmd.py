"""
Tests unitarios para ProvedorCmd
"""

from unittest.mock import MagicMock, patch

import pytest
from src.dominio.entities.provedor import Pais, Provedor
from src.infraestructura.cmd.provedor_cmd import ProvedorCmd


class TestProvedorCmd:
    """Tests para ProvedorCmd"""

    @patch("src.infraestructura.cmd.provedor_cmd.ProvedorMapper")
    def test_obtener_todos_los_provedores_exitoso(self, mock_mapper, app_context):
        """Test de obtener todos los proveedores exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
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
        mock_use_case.obtener_todos_los_provedores.return_value = provedores

        mock_dto = MagicMock()
        mock_dict = {"id": 1, "nombre": "Proveedor 1"}
        mock_mapper.entities_to_dtos.return_value = [mock_dto]
        mock_mapper.dtos_to_dicts.return_value = [mock_dict]

        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_todos_los_provedores()

        # Assert
        assert status_code == 200
        mock_use_case.obtener_todos_los_provedores.assert_called_once()

    def test_obtener_todos_los_provedores_error(self, app_context):
        """Test de obtener todos los proveedores con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_todos_los_provedores.side_effect = Exception("Error de base de datos")
        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_todos_los_provedores()

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

    @patch("src.infraestructura.cmd.provedor_cmd.ProvedorMapper")
    def test_obtener_provedor_por_id_exitoso(self, mock_mapper, app_context):
        """Test de obtener proveedor por ID exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
        provedor = Provedor(
            id=1,
            nit=900123456,
            nombre="Proveedor Test",
            pais=Pais.COLOMBIA,
            direccion="Calle 123",
            telefono=6012345678,
            email="proveedor@test.com",
        )
        mock_use_case.obtener_provedor_por_id.return_value = provedor

        mock_dto = MagicMock()
        mock_dict = {"id": 1, "nombre": "Proveedor Test"}
        mock_mapper.entity_to_dto.return_value = mock_dto
        mock_mapper.dto_to_dict.return_value = mock_dict

        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedor_por_id(1)

        # Assert
        assert status_code == 200
        mock_use_case.obtener_provedor_por_id.assert_called_once_with(1)

    def test_obtener_provedor_por_id_no_encontrado(self, app_context):
        """Test de obtener proveedor por ID cuando no existe"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_provedor_por_id.return_value = None
        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedor_por_id(999)

        # Assert
        assert status_code == 404
        assert "error" in response.get_json()
        mock_use_case.obtener_provedor_por_id.assert_called_once_with(999)

    def test_obtener_provedor_por_id_error(self, app_context):
        """Test de obtener proveedor por ID con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_provedor_por_id.side_effect = Exception("Error de base de datos")
        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedor_por_id(1)

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

    @patch("src.infraestructura.cmd.provedor_cmd.ProvedorMapper")
    def test_obtener_provedor_por_nit_exitoso(self, mock_mapper, app_context):
        """Test de obtener proveedor por NIT exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
        provedor = Provedor(
            id=1,
            nit=900123456,
            nombre="Proveedor Test",
            pais=Pais.COLOMBIA,
            direccion="Calle 123",
            telefono=6012345678,
            email="proveedor@test.com",
        )
        mock_use_case.obtener_provedor_por_nit.return_value = provedor

        mock_dto = MagicMock()
        mock_dict = {"id": 1, "nit": 900123456}
        mock_mapper.entity_to_dto.return_value = mock_dto
        mock_mapper.dto_to_dict.return_value = mock_dict

        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedor_por_nit(900123456)

        # Assert
        assert status_code == 200
        mock_use_case.obtener_provedor_por_nit.assert_called_once_with(900123456)

    def test_obtener_provedor_por_nit_no_encontrado(self, app_context):
        """Test de obtener proveedor por NIT cuando no existe"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_provedor_por_nit.return_value = None
        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedor_por_nit(999999999)

        # Assert
        assert status_code == 404
        assert "error" in response.get_json()
        mock_use_case.obtener_provedor_por_nit.assert_called_once_with(999999999)

    def test_obtener_provedor_por_nit_error(self, app_context):
        """Test de obtener proveedor por NIT con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_provedor_por_nit.side_effect = Exception("Error de base de datos")
        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedor_por_nit(900123456)

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

    @patch("src.infraestructura.cmd.provedor_cmd.ProvedorMapper")
    def test_obtener_provedores_por_pais_exitoso(self, mock_mapper, app_context):
        """Test de obtener proveedores por país exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
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
        mock_use_case.obtener_provedores_por_pais.return_value = provedores

        mock_dto = MagicMock()
        mock_dict = {"id": 1, "pais": "colombia"}
        mock_mapper.entities_to_dtos.return_value = [mock_dto]
        mock_mapper.dtos_to_dicts.return_value = [mock_dict]

        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedores_por_pais("colombia")

        # Assert
        assert status_code == 200
        mock_use_case.obtener_provedores_por_pais.assert_called_once_with("colombia")

    def test_obtener_provedores_por_pais_error(self, app_context):
        """Test de obtener proveedores por país con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.obtener_provedores_por_pais.side_effect = Exception("Error de base de datos")
        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.obtener_provedores_por_pais("colombia")

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()

    @patch("src.infraestructura.cmd.provedor_cmd.ProvedorMapper")
    def test_buscar_provedores_por_nombre_exitoso(self, mock_mapper, app_context):
        """Test de buscar proveedores por nombre exitosamente"""
        # Arrange
        mock_use_case = MagicMock()
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
        mock_use_case.buscar_provedores_por_nombre.return_value = provedores

        mock_dto = MagicMock()
        mock_dict = {"id": 1, "nombre": "Tecnología Avanzada"}
        mock_mapper.entities_to_dtos.return_value = [mock_dto]
        mock_mapper.dtos_to_dicts.return_value = [mock_dict]

        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.buscar_provedores_por_nombre("Tecnología")

        # Assert
        assert status_code == 200
        mock_use_case.buscar_provedores_por_nombre.assert_called_once_with("Tecnología")

    def test_buscar_provedores_por_nombre_error(self, app_context):
        """Test de buscar proveedores por nombre con error"""
        # Arrange
        mock_use_case = MagicMock()
        mock_use_case.buscar_provedores_por_nombre.side_effect = Exception("Error de base de datos")
        cmd = ProvedorCmd(mock_use_case)

        # Act
        response, status_code = cmd.buscar_provedores_por_nombre("Tecnología")

        # Assert
        assert status_code == 500
        assert "error" in response.get_json()
