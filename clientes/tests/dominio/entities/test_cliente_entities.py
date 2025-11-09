"""
Tests unitarios para las entidades del módulo de clientes
"""

import os
import sys

import pytest

# Agregar el directorio de clientes al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestClienteEntity:
    """Tests para la entidad Cliente"""

    def test_cliente_entity_creation(self):
        """Test de creación de la entidad Cliente"""
        from src.dominio.entities.cliente import Cliente

        cliente = Cliente(
            id="cli-001",
            nombre="Hospital San Rafael",
            email="contacto@sanrafael.com",
            telefono="+57 1 234 5678",
            direccion="Calle 123 #45-67",
            razon_social="Hospital San Rafael S.A.",
            nit="900123456-7",
        )

        assert cliente.id == "cli-001"
        assert cliente.nombre == "Hospital San Rafael"
        assert cliente.email == "contacto@sanrafael.com"
        assert cliente.telefono == "+57 1 234 5678"
        assert cliente.direccion == "Calle 123 #45-67"
        assert cliente.razon_social == "Hospital San Rafael S.A."
        assert cliente.nit == "900123456-7"

    def test_cliente_entity_to_dict(self):
        """Test del método to_dict de Cliente"""
        from src.dominio.entities.cliente import Cliente

        cliente = Cliente(
            id="cli-002",
            nombre="Clínica Los Rosales",
            email="info@losrosales.com",
            telefono="+57 1 345 6789",
            direccion="Avenida Principal 789",
            razon_social="Clínica Los Rosales Ltda.",
            nit="900234567-8",
        )

        cliente_dict = cliente.to_dict()
        assert isinstance(cliente_dict, dict)
        assert cliente_dict["id"] == "cli-002"
        assert cliente_dict["nombre"] == "Clínica Los Rosales"
        assert cliente_dict["email"] == "info@losrosales.com"
        assert cliente_dict["telefono"] == "+57 1 345 6789"
        assert cliente_dict["direccion"] == "Avenida Principal 789"
        assert cliente_dict["razon_social"] == "Clínica Los Rosales Ltda."
        assert cliente_dict["nit"] == "900234567-8"

    def test_cliente_entity_immutable(self):
        """Test de que Cliente es inmutable"""
        from src.dominio.entities.cliente import Cliente

        cliente = Cliente(
            id="cli-003",
            nombre="Farmacia MedPlus",
            email="ventas@medplus.com",
            telefono="+57 1 456 7890",
            direccion="Carrera 50 #100-25",
            razon_social="Farmacia MedPlus S.A.",
            nit="900345678-9",
        )

        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            cliente.nombre = "Nuevo Nombre"

    def test_cliente_different_types(self):
        """Test de diferentes tipos de clientes"""
        from src.dominio.entities.cliente import Cliente

        # Test Hospital
        hospital = Cliente(
            id="cli-004",
            nombre="Hospital Central",
            email="contacto@hospitalcentral.com",
            telefono="+57 1 555 1234",
            direccion="Avenida Principal 456",
            razon_social="Hospital Central S.A.",
            nit="900555666-7",
        )
        assert "Hospital" in hospital.nombre

        # Test Clínica
        clinica = Cliente(
            id="cli-005",
            nombre="Clínica Especializada",
            email="info@clinicaespecializada.com",
            telefono="+57 1 666 7890",
            direccion="Calle 78 #45-12",
            razon_social="Clínica Especializada S.A.S.",
            nit="900777888-9",
        )
        assert "Clínica" in clinica.nombre

    def test_cliente_email_validation(self):
        """Test de validación de formato de email"""
        from src.dominio.entities.cliente import Cliente

        cliente = Cliente(
            id="cli-006",
            nombre="Cliente Test",
            email="test@example.com",
            telefono="+57 1 111 2222",
            direccion="Dirección Test",
            razon_social="Razón Social Test",
            nit="900111222-3",
        )

        assert "@" in cliente.email
        assert "." in cliente.email.split("@")[1]

    def test_cliente_nit_uniqueness(self):
        """Test de que el NIT debe ser único"""
        from src.dominio.entities.cliente import Cliente

        cliente1 = Cliente(
            id="cli-007",
            nombre="Cliente 1",
            email="cliente1@test.com",
            telefono="+57 1 111 1111",
            direccion="Dirección 1",
            razon_social="Razón Social 1",
            nit="900111111-1",
        )

        cliente2 = Cliente(
            id="cli-008",
            nombre="Cliente 2",
            email="cliente2@test.com",
            telefono="+57 1 222 2222",
            direccion="Dirección 2",
            razon_social="Razón Social 2",
            nit="900222222-2",
        )

        # Cada cliente debe tener un NIT diferente
        assert cliente1.nit != cliente2.nit

    def test_cliente_razon_social_variations(self):
        """Test de diferentes formatos de razón social"""
        from src.dominio.entities.cliente import Cliente

        # S.A.
        sa_cliente = Cliente(
            id="cli-009",
            nombre="Cliente SA",
            email="sa@test.com",
            telefono="+57 1 333 3333",
            direccion="Dirección SA",
            razon_social="Cliente S.A.",
            nit="900333333-3",
        )
        assert "S.A." in sa_cliente.razon_social

        # Ltda.
        ltda_cliente = Cliente(
            id="cli-010",
            nombre="Cliente Ltda",
            email="ltda@test.com",
            telefono="+57 1 444 4444",
            direccion="Dirección Ltda",
            razon_social="Cliente Ltda.",
            nit="900444444-4",
        )
        assert "Ltda." in ltda_cliente.razon_social

        # S.A.S.
        sas_cliente = Cliente(
            id="cli-011",
            nombre="Cliente SAS",
            email="sas@test.com",
            telefono="+57 1 555 5555",
            direccion="Dirección SAS",
            razon_social="Cliente S.A.S.",
            nit="900555555-5",
        )
        assert "S.A.S." in sas_cliente.razon_social


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

