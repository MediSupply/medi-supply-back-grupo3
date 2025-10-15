"""
Tests unitarios para los DTOs del módulo de provedores
"""

import os
import sys

import pytest

# Agregar el directorio de provedores al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestProvedorDto:
    """Tests para el ProvedorDto"""

    def test_provedor_dto_creation(self):
        """Test de creación del ProvedorDto"""
        from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto

        provedor_dto = ProvedorDto(
            id=1,
            nit=123456789,
            nombre="Proveedor Test",
            pais=PaisDto.COLOMBIA,
            direccion="Calle 123 #45-67",
            telefono=3001234567,
            email="proveedor@test.com",
        )

        assert provedor_dto.id == 1
        assert provedor_dto.nit == 123456789
        assert provedor_dto.nombre == "Proveedor Test"
        assert provedor_dto.pais == PaisDto.COLOMBIA
        assert provedor_dto.direccion == "Calle 123 #45-67"
        assert provedor_dto.telefono == 3001234567
        assert provedor_dto.email == "proveedor@test.com"

    def test_provedor_dto_immutable(self):
        """Test de que ProvedorDto es inmutable"""
        from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto

        provedor_dto = ProvedorDto(
            id=2,
            nit=987654321,
            nombre="Proveedor Inmutable",
            pais=PaisDto.MEXICO,
            direccion="Av. Principal 456",
            telefono=5551234567,
            email="inmutable@test.com",
        )

        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            provedor_dto.nombre = "Nuevo Nombre"

    def test_provedor_dto_pais_enum(self):
        """Test de los valores del enum PaisDto"""
        from src.aplicacion.dtos.provedor_dto import PaisDto

        assert PaisDto.COLOMBIA.value == "colombia"
        assert PaisDto.MEXICO.value == "mexico"
        assert PaisDto.ARGENTINA.value == "argentina"
        assert PaisDto.CHILE.value == "chile"
        assert PaisDto.PERU.value == "peru"
        assert PaisDto.BRASIL.value == "brasil"
        assert PaisDto.ECUADOR.value == "ecuador"
        assert PaisDto.VENEZUELA.value == "venezuela"
        assert PaisDto.URUGUAY.value == "uruguay"
        assert PaisDto.PARAGUAY.value == "paraguay"
        assert PaisDto.BOLIVIA.value == "bolivia"
        assert PaisDto.OTROS.value == "otros"

    def test_provedor_dto_different_countries(self):
        """Test de diferentes países"""
        from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto

        # Test ARGENTINA
        argentina_dto = ProvedorDto(
            id=3,
            nit=111222333,
            nombre="Proveedor Argentina",
            pais=PaisDto.ARGENTINA,
            direccion="Buenos Aires, Argentina",
            telefono=54111234567,
            email="argentina@test.com",
        )
        assert argentina_dto.pais == PaisDto.ARGENTINA

        # Test CHILE
        chile_dto = ProvedorDto(
            id=4,
            nit=444555666,
            nombre="Proveedor Chile",
            pais=PaisDto.CHILE,
            direccion="Santiago, Chile",
            telefono=56987654321,
            email="chile@test.com",
        )
        assert chile_dto.pais == PaisDto.CHILE

        # Test ECUADOR
        ecuador_dto = ProvedorDto(
            id=5,
            nit=777888999,
            nombre="Proveedor Ecuador",
            pais=PaisDto.ECUADOR,
            direccion="Quito, Ecuador",
            telefono=593987654321,
            email="ecuador@test.com",
        )
        assert ecuador_dto.pais == PaisDto.ECUADOR

    def test_provedor_dto_numeric_fields(self):
        """Test de campos numéricos"""
        from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto

        provedor_dto = ProvedorDto(
            id=6,
            nit=123456789,
            nombre="Proveedor Numérico",
            pais=PaisDto.PERU,
            direccion="Lima, Perú",
            telefono=51987654321,
            email="numerico@test.com",
        )

        assert isinstance(provedor_dto.id, int)
        assert isinstance(provedor_dto.nit, int)
        assert isinstance(provedor_dto.telefono, int)

        # Test valores específicos
        assert provedor_dto.id == 6
        assert provedor_dto.nit == 123456789
        assert provedor_dto.telefono == 51987654321

    def test_provedor_dto_string_fields(self):
        """Test de campos de texto"""
        from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto

        provedor_dto = ProvedorDto(
            id=7,
            nit=987654321,
            nombre="Proveedor Texto",
            pais=PaisDto.VENEZUELA,
            direccion="Caracas, Venezuela - Av. Bolívar 123",
            telefono=584121234567,
            email="texto@proveedor.com",
        )

        assert isinstance(provedor_dto.nombre, str)
        assert isinstance(provedor_dto.direccion, str)
        assert isinstance(provedor_dto.email, str)

        # Test valores específicos
        assert provedor_dto.nombre == "Proveedor Texto"
        assert provedor_dto.direccion == "Caracas, Venezuela - Av. Bolívar 123"
        assert provedor_dto.email == "texto@proveedor.com"

    def test_provedor_dto_edge_cases(self):
        """Test de casos límite"""
        from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto

        # Test con valores mínimos
        min_dto = ProvedorDto(id=1, nit=1, nombre="A", pais=PaisDto.OTROS, direccion="A", telefono=1, email="a@a.com")

        assert min_dto.id == 1
        assert min_dto.nit == 1
        assert min_dto.nombre == "A"
        assert min_dto.telefono == 1
        assert min_dto.email == "a@a.com"

        # Test con valores grandes
        max_dto = ProvedorDto(
            id=999999,
            nit=999999999,
            nombre="Proveedor con Nombre Muy Largo para Testing de DTOs",
            pais=PaisDto.BRASIL,
            direccion="Dirección muy larga con muchos detalles y especificaciones para testing",
            telefono=9999999999,
            email="proveedor.muy.largo@dominio.extenso.com",
        )

        assert max_dto.id == 999999
        assert max_dto.nit == 999999999
        assert len(max_dto.nombre) > 20
        assert len(max_dto.direccion) > 30
        assert len(max_dto.email) > 20

    def test_provedor_dto_south_american_countries(self):
        """Test específico de países sudamericanos"""
        from src.aplicacion.dtos.provedor_dto import PaisDto, ProvedorDto

        countries = [
            PaisDto.COLOMBIA,
            PaisDto.ARGENTINA,
            PaisDto.CHILE,
            PaisDto.PERU,
            PaisDto.BRASIL,
            PaisDto.ECUADOR,
            PaisDto.VENEZUELA,
            PaisDto.URUGUAY,
            PaisDto.PARAGUAY,
            PaisDto.BOLIVIA,
        ]

        for i, country in enumerate(countries, 1):
            provedor_dto = ProvedorDto(
                id=i,
                nit=100000000 + i,
                nombre=f"Proveedor {country.value.title()}",
                pais=country,
                direccion=f"Capital de {country.value.title()}",
                telefono=1000000000 + i,
                email=f"{country.value}@test.com",
            )

            assert provedor_dto.pais == country
            assert provedor_dto.nombre == f"Proveedor {country.value.title()}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
