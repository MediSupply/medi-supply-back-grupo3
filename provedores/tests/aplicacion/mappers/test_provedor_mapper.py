"""
Tests unitarios para ProvedorMapper
"""

import pytest
from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto
from src.aplicacion.mappers.provedor_mapper import ProvedorMapper
from src.dominio.entities.provedor import Pais, Provedor


class TestProvedorMapper:
    """Tests para ProvedorMapper"""

    def test_entity_to_dto(self, sample_provedor):
        """Test de conversión de Entity a DTO"""
        dto = ProvedorMapper.entity_to_dto(sample_provedor)

        assert isinstance(dto, ProvedorDto)
        assert dto.id == 1
        assert dto.nit == 900123456
        assert dto.nombre == "Tecnología Avanzada S.A.S"
        assert dto.pais == PaisDto.COLOMBIA
        assert dto.email == "contacto@tecnologiaavanzada.com"

    def test_dto_to_entity(self, sample_provedor_dto):
        """Test de conversión de DTO a Entity"""
        entity = ProvedorMapper.dto_to_entity(sample_provedor_dto)

        assert isinstance(entity, Provedor)
        assert entity.id == 1
        assert entity.nit == 900123456
        assert entity.nombre == "Tecnología Avanzada S.A.S"
        assert entity.pais == Pais.COLOMBIA
        assert entity.email == "contacto@tecnologiaavanzada.com"

    def test_entities_to_dtos(self, sample_provedor):
        """Test de conversión de lista de entidades a lista de DTOs"""
        provedores = [
            sample_provedor,
            Provedor(
                id=2,
                nit=800987654,
                nombre="Distribuidora Nacional",
                pais=Pais.COLOMBIA,
                direccion="Medellín",
                telefono=6045678901,
                email="ventas@distribuidora.com",
            ),
        ]
        dtos = ProvedorMapper.entities_to_dtos(provedores)

        assert len(dtos) == 2
        assert isinstance(dtos[0], ProvedorDto)
        assert isinstance(dtos[1], ProvedorDto)
        assert dtos[0].id == 1
        assert dtos[1].id == 2

    def test_dto_to_dict(self, sample_provedor_dto):
        """Test de conversión de DTO a diccionario"""
        dict_data = ProvedorMapper.dto_to_dict(sample_provedor_dto)

        assert isinstance(dict_data, dict)
        assert dict_data["id"] == 1
        assert dict_data["nit"] == 900123456
        assert dict_data["nombre"] == "Tecnología Avanzada S.A.S"
        assert dict_data["pais"] == "colombia"
        assert dict_data["email"] == "contacto@tecnologiaavanzada.com"

    def test_dtos_to_dicts(self, sample_provedor_dto):
        """Test de conversión de lista de DTOs a lista de diccionarios"""
        dtos = [
            sample_provedor_dto,
            ProvedorDto(
                id=2,
                nit=800987654,
                nombre="Distribuidora Nacional",
                pais=PaisDto.COLOMBIA,
                direccion="Medellín",
                telefono=6045678901,
                email="ventas@distribuidora.com",
            ),
        ]
        dicts = ProvedorMapper.dtos_to_dicts(dtos)

        assert len(dicts) == 2
        assert isinstance(dicts[0], dict)
        assert isinstance(dicts[1], dict)
        assert dicts[0]["id"] == 1
        assert dicts[1]["id"] == 2

    def test_round_trip_entity_dto(self, sample_provedor):
        """Test de ida y vuelta: Entity -> DTO -> Entity"""
        dto = ProvedorMapper.entity_to_dto(sample_provedor)
        entity = ProvedorMapper.dto_to_entity(dto)

        assert entity.id == sample_provedor.id
        assert entity.nit == sample_provedor.nit
        assert entity.nombre == sample_provedor.nombre
        assert entity.pais == sample_provedor.pais
        assert entity.direccion == sample_provedor.direccion
        assert entity.telefono == sample_provedor.telefono
        assert entity.email == sample_provedor.email

    def test_mapper_with_different_paises(self):
        """Test del mapper con diferentes países"""
        # Test con MEXICO
        provedor_mexico = Provedor(
            id=3,
            nit=123456789,
            nombre="Proveedor México",
            pais=Pais.MEXICO,
            direccion="Ciudad de México",
            telefono=525512345678,
            email="mexico@test.com",
        )
        dto = ProvedorMapper.entity_to_dto(provedor_mexico)
        assert dto.pais == PaisDto.MEXICO

        # Test con BRASIL
        provedor_brasil = Provedor(
            id=4,
            nit=987654321,
            nombre="Proveedor Brasil",
            pais=Pais.BRASIL,
            direccion="São Paulo",
            telefono=5511987654321,
            email="brasil@test.com",
        )
        dto = ProvedorMapper.entity_to_dto(provedor_brasil)
        assert dto.pais == PaisDto.BRASIL

    def test_mapper_with_different_values(self):
        """Test del mapper con diferentes valores"""
        provedor = Provedor(
            id=999,
            nit=555666777,
            nombre="Proveedor Test",
            pais=Pais.ARGENTINA,
            direccion="Buenos Aires",
            telefono=54111234567,
            email="test@proveedor.com",
        )

        dto = ProvedorMapper.entity_to_dto(provedor)
        assert dto.id == 999
        assert dto.pais == PaisDto.ARGENTINA
        assert dto.nit == 555666777

        dict_data = ProvedorMapper.dto_to_dict(dto)
        assert dict_data["id"] == 999
        assert dict_data["pais"] == "argentina"

    def test_entities_to_dtos_empty_list(self):
        """Test de conversión de lista vacía de entidades"""
        provedores = []
        dtos = ProvedorMapper.entities_to_dtos(provedores)

        assert len(dtos) == 0
        assert isinstance(dtos, list)

    def test_dtos_to_dicts_empty_list(self):
        """Test de conversión de lista vacía de DTOs"""
        dtos = []
        dicts = ProvedorMapper.dtos_to_dicts(dtos)

        assert len(dicts) == 0
        assert isinstance(dicts, list)
