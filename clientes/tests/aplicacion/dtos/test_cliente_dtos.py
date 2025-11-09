"""
Tests unitarios para los DTOs del módulo de clientes
"""

import os
import sys

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteDto:
    """Tests para el ClienteDto"""

    def test_cliente_dto_creation(self):
        """Test de creación del ClienteDto"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto

        cliente_dto = ClienteDto(
            id="cli-001",
            nombre="Hospital San Rafael",
            email="contacto@sanrafael.com",
            telefono="+57 1 234 5678",
            direccion="Calle 123 #45-67",
            razon_social="Hospital San Rafael S.A.",
            nit="900123456-7",
        )

        assert cliente_dto.id == "cli-001"
        assert cliente_dto.nombre == "Hospital San Rafael"
        assert cliente_dto.email == "contacto@sanrafael.com"
        assert cliente_dto.telefono == "+57 1 234 5678"
        assert cliente_dto.direccion == "Calle 123 #45-67"
        assert cliente_dto.razon_social == "Hospital San Rafael S.A."
        assert cliente_dto.nit == "900123456-7"

    def test_cliente_dto_immutable(self):
        """Test de que ClienteDto es inmutable"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto

        cliente_dto = ClienteDto(
            id="cli-002",
            nombre="Clínica Los Rosales",
            email="info@losrosales.com",
            telefono="+57 1 345 6789",
            direccion="Avenida Principal 789",
            razon_social="Clínica Los Rosales Ltda.",
            nit="900234567-8",
        )

        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            cliente_dto.nombre = "Nuevo Nombre"

    def test_cliente_dto_different_types(self):
        """Test de diferentes tipos de clientes"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto

        # Test Hospital
        hospital = ClienteDto(
            id="cli-003",
            nombre="Hospital Central",
            email="contacto@hospitalcentral.com",
            telefono="+57 1 555 1234",
            direccion="Avenida Principal 456",
            razon_social="Hospital Central S.A.",
            nit="900555666-7",
        )
        assert "Hospital" in hospital.nombre

        # Test Clínica
        clinica = ClienteDto(
            id="cli-004",
            nombre="Clínica Especializada",
            email="info@clinicaespecializada.com",
            telefono="+57 1 666 7890",
            direccion="Calle 78 #45-12",
            razon_social="Clínica Especializada S.A.S.",
            nit="900777888-9",
        )
        assert "Clínica" in clinica.nombre

        # Test Farmacia
        farmacia = ClienteDto(
            id="cli-005",
            nombre="Farmacia MedPlus",
            email="ventas@medplus.com",
            telefono="+57 1 456 7890",
            direccion="Carrera 50 #100-25",
            razon_social="Farmacia MedPlus S.A.",
            nit="900345678-9",
        )
        assert "Farmacia" in farmacia.nombre

    def test_cliente_dto_email_format(self):
        """Test de formato de email"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto

        cliente_dto = ClienteDto(
            id="cli-006",
            nombre="Cliente Test",
            email="test@example.com",
            telefono="+57 1 111 2222",
            direccion="Dirección Test",
            razon_social="Razón Social Test",
            nit="900111222-3",
        )

        assert "@" in cliente_dto.email
        assert cliente_dto.email.endswith(".com")

    def test_cliente_dto_nit_format(self):
        """Test de formato de NIT"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto

        cliente_dto = ClienteDto(
            id="cli-007",
            nombre="Cliente Test",
            email="test@example.com",
            telefono="+57 1 111 2222",
            direccion="Dirección Test",
            razon_social="Razón Social Test",
            nit="900111222-3",
        )

        # NIT típico colombiano: números-guion-digito
        assert "-" in cliente_dto.nit
        assert len(cliente_dto.nit.split("-")) == 2

    def test_cliente_dto_telefono_format(self):
        """Test de formato de teléfono"""
        from src.aplicacion.dtos.cliente_dto import ClienteDto

        cliente_dto = ClienteDto(
            id="cli-008",
            nombre="Cliente Test",
            email="test@example.com",
            telefono="+57 1 111 2222",
            direccion="Dirección Test",
            razon_social="Razón Social Test",
            nit="900111222-3",
        )

        # Teléfono típico colombiano con código de país
        assert cliente_dto.telefono.startswith("+57")
        assert len(cliente_dto.telefono) >= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

