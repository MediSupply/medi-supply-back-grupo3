"""
Tests unitarios para los mappers del módulo de clientes
"""

import os
import sys
import uuid

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteMapper:
    """Tests para ClienteMapper"""

    def test_json_to_dto(self):
        """Test de conversión de JSON a DTO"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto
        from src.aplicacion.mappers.cliente_mapper import ClienteMapper

        json_data = {
            "id": "cli-001",
            "nombre": "Hospital San Rafael",
            "email": "contacto@sanrafael.com",
            "telefono": "+57 1 234 5678",
            "direccion": "Calle 123 #45-67",
            "razon_social": "Hospital San Rafael S.A.",
            "nit": "900123456-7",
        }

        cliente_dto = ClienteMapper.json_to_dto(json_data)

        assert isinstance(cliente_dto, ClienteDto)
        assert cliente_dto.id == "cli-001"
        assert cliente_dto.nombre == "Hospital San Rafael"
        assert cliente_dto.email == "contacto@sanrafael.com"

    def test_json_to_dto_generates_id(self):
        """Test de que genera ID cuando no se proporciona"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto
        from src.aplicacion.mappers.cliente_mapper import ClienteMapper

        json_data = {
            "nombre": "Hospital Nuevo",
            "email": "contacto@hospitalnuevo.com",
            "telefono": "+57 1 999 9999",
            "direccion": "Calle Nueva 123",
            "razon_social": "Hospital Nuevo S.A.",
            "nit": "900999999-9",
        }

        cliente_dto = ClienteMapper.json_to_dto(json_data)

        assert isinstance(cliente_dto, ClienteDto)
        assert cliente_dto.id is not None
        assert cliente_dto.id != ""
        # Verificar que es un UUID válido
        try:
            uuid.UUID(cliente_dto.id)
        except ValueError:
            pytest.fail(f"Generated ID '{cliente_dto.id}' is not a valid UUID")

    def test_dto_to_json(self):
        """Test de conversión de DTO a JSON"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto
        from src.aplicacion.mappers.cliente_mapper import ClienteMapper

        cliente_dto = ClienteDto(
            id="cli-002",
            nombre="Clínica Los Rosales",
            email="info@losrosales.com",
            telefono="+57 1 345 6789",
            direccion="Avenida Principal 789",
            razon_social="Clínica Los Rosales Ltda.",
            nit="900234567-8",
        )

        json_data = ClienteMapper.dto_to_json(cliente_dto)

        assert isinstance(json_data, dict)
        assert json_data["id"] == "cli-002"
        assert json_data["nombre"] == "Clínica Los Rosales"
        assert json_data["email"] == "info@losrosales.com"
        assert json_data["telefono"] == "+57 1 345 6789"
        assert json_data["direccion"] == "Avenida Principal 789"
        assert json_data["razon_social"] == "Clínica Los Rosales Ltda."
        assert json_data["nit"] == "900234567-8"

    def test_dto_to_entity(self):
        """Test de conversión de DTO a Entity"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto
        from src.aplicacion.mappers.cliente_mapper import ClienteMapper
        from src.dominio.entities.cliente import Cliente

        cliente_dto = ClienteDto(
            id="cli-003",
            nombre="Farmacia MedPlus",
            email="ventas@medplus.com",
            telefono="+57 1 456 7890",
            direccion="Carrera 50 #100-25",
            razon_social="Farmacia MedPlus S.A.",
            nit="900345678-9",
        )

        cliente = ClienteMapper.dto_to_entity(cliente_dto)

        assert isinstance(cliente, Cliente)
        assert cliente.id == "cli-003"
        assert cliente.nombre == "Farmacia MedPlus"
        assert cliente.email == "ventas@medplus.com"

    def test_entity_to_dto(self):
        """Test de conversión de Entity a DTO"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto
        from src.aplicacion.mappers.cliente_mapper import ClienteMapper
        from src.dominio.entities.cliente import Cliente

        cliente = Cliente(
            id="cli-004",
            nombre="Hospital Central",
            email="contacto@hospitalcentral.com",
            telefono="+57 1 555 1234",
            direccion="Avenida Principal 456",
            razon_social="Hospital Central S.A.",
            nit="900555666-7",
        )

        cliente_dto = ClienteMapper.entity_to_dto(cliente)

        assert isinstance(cliente_dto, ClienteDto)
        assert cliente_dto.id == "cli-004"
        assert cliente_dto.nombre == "Hospital Central"
        assert cliente_dto.email == "contacto@hospitalcentral.com"

    def test_round_trip_mapping(self):
        """Test de ida y vuelta: Entity -> DTO -> Entity"""
        from src.aplicacion.mappers.cliente_mapper import ClienteMapper
        from src.dominio.entities.cliente import Cliente

        cliente_original = Cliente(
            id="cli-005",
            nombre="Cliente Test",
            email="test@example.com",
            telefono="+57 1 111 2222",
            direccion="Dirección Test",
            razon_social="Razón Social Test",
            nit="900111222-3",
        )

        # Entity -> DTO -> Entity
        cliente_dto = ClienteMapper.entity_to_dto(cliente_original)
        cliente_resultado = ClienteMapper.dto_to_entity(cliente_dto)

        assert cliente_resultado.id == cliente_original.id
        assert cliente_resultado.nombre == cliente_original.nombre
        assert cliente_resultado.email == cliente_original.email
        assert cliente_resultado.telefono == cliente_original.telefono
        assert cliente_resultado.direccion == cliente_original.direccion
        assert cliente_resultado.razon_social == cliente_original.razon_social
        assert cliente_resultado.nit == cliente_original.nit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
