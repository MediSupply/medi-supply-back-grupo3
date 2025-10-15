"""
Tests unitarios para las entidades del módulo de provedores
"""

import os
import sys

import pytest

# Agregar el directorio de provedores al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))


class TestProvedorEntity:
    """Tests para la entidad Provedor"""

    def test_provedor_entity_creation(self):
        """Test de creación de la entidad Provedor"""
        from src.dominio.entities.provedor import Pais, Provedor

        provedor = Provedor(
            id=1,
            nit=123456789,
            nombre="Proveedor Test",
            pais=Pais.COLOMBIA,
            direccion="Calle 123 #45-67",
            telefono=3001234567,
            email="proveedor@test.com",
        )

        assert provedor.id == 1
        assert provedor.nit == 123456789
        assert provedor.nombre == "Proveedor Test"
        assert provedor.pais == Pais.COLOMBIA
        assert provedor.direccion == "Calle 123 #45-67"
        assert provedor.telefono == 3001234567
        assert provedor.email == "proveedor@test.com"

    def test_provedor_entity_to_dict(self):
        """Test del método to_dict de Provedor"""
        from src.dominio.entities.provedor import Pais, Provedor

        provedor = Provedor(
            id=2,
            nit=987654321,
            nombre="Proveedor Export",
            pais=Pais.MEXICO,
            direccion="Av. Principal 456",
            telefono=5551234567,
            email="export@proveedor.com",
        )

        provedor_dict = provedor.to_dict()
        assert isinstance(provedor_dict, dict)
        assert provedor_dict["id"] == 2
        assert provedor_dict["nit"] == 987654321
        assert provedor_dict["nombre"] == "Proveedor Export"
        assert provedor_dict["pais"] == "mexico"
        assert provedor_dict["direccion"] == "Av. Principal 456"
        assert provedor_dict["telefono"] == 5551234567
        assert provedor_dict["email"] == "export@proveedor.com"

    def test_provedor_entity_immutable(self):
        """Test de que Provedor es inmutable"""
        from src.dominio.entities.provedor import Pais, Provedor

        provedor = Provedor(
            id=3,
            nit=111222333,
            nombre="Proveedor Inmutable",
            pais=Pais.ARGENTINA,
            direccion="Calle Falsa 123",
            telefono=54111234567,
            email="inmutable@test.com",
        )

        # Verificar que es inmutable (frozen dataclass)
        with pytest.raises(AttributeError):
            provedor.nombre = "Nuevo Nombre"

    def test_provedor_pais_enum(self):
        """Test de los valores del enum Pais"""
        from src.dominio.entities.provedor import Pais

        assert Pais.COLOMBIA.value == "colombia"
        assert Pais.MEXICO.value == "mexico"
        assert Pais.ARGENTINA.value == "argentina"
        assert Pais.CHILE.value == "chile"
        assert Pais.PERU.value == "peru"
        assert Pais.BRASIL.value == "brasil"
        assert Pais.ECUADOR.value == "ecuador"
        assert Pais.VENEZUELA.value == "venezuela"
        assert Pais.URUGUAY.value == "uruguay"
        assert Pais.PARAGUAY.value == "paraguay"
        assert Pais.BOLIVIA.value == "bolivia"
        assert Pais.OTROS.value == "otros"

    def test_provedor_different_countries(self):
        """Test de diferentes países"""
        from src.dominio.entities.provedor import Pais, Provedor

        # Test COLOMBIA
        colombia_prov = Provedor(
            id=4,
            nit=123456789,
            nombre="Proveedor Colombia",
            pais=Pais.COLOMBIA,
            direccion="Bogotá, Colombia",
            telefono=3001234567,
            email="colombia@test.com",
        )
        assert colombia_prov.pais == Pais.COLOMBIA

        # Test BRASIL
        brasil_prov = Provedor(
            id=5,
            nit=987654321,
            nombre="Proveedor Brasil",
            pais=Pais.BRASIL,
            direccion="São Paulo, Brasil",
            telefono=5511987654321,
            email="brasil@test.com",
        )
        assert brasil_prov.pais == Pais.BRASIL

        # Test OTROS
        otros_prov = Provedor(
            id=6,
            nit=555666777,
            nombre="Proveedor Internacional",
            pais=Pais.OTROS,
            direccion="Dirección Internacional",
            telefono=1234567890,
            email="internacional@test.com",
        )
        assert otros_prov.pais == Pais.OTROS

    def test_provedor_numeric_fields(self):
        """Test de campos numéricos"""
        from src.dominio.entities.provedor import Pais, Provedor

        provedor = Provedor(
            id=7,
            nit=999888777,
            nombre="Proveedor Numérico",
            pais=Pais.CHILE,
            direccion="Santiago, Chile",
            telefono=56987654321,
            email="numerico@test.com",
        )

        assert isinstance(provedor.id, int)
        assert isinstance(provedor.nit, int)
        assert isinstance(provedor.telefono, int)

        # Test valores específicos
        assert provedor.id == 7
        assert provedor.nit == 999888777
        assert provedor.telefono == 56987654321

    def test_provedor_string_fields(self):
        """Test de campos de texto"""
        from src.dominio.entities.provedor import Pais, Provedor

        provedor = Provedor(
            id=8,
            nit=444555666,
            nombre="Proveedor Texto",
            pais=Pais.PERU,
            direccion="Lima, Perú - Av. Principal 123",
            telefono=51987654321,
            email="texto@proveedor.com",
        )

        assert isinstance(provedor.nombre, str)
        assert isinstance(provedor.direccion, str)
        assert isinstance(provedor.email, str)

        # Test valores específicos
        assert provedor.nombre == "Proveedor Texto"
        assert provedor.direccion == "Lima, Perú - Av. Principal 123"
        assert provedor.email == "texto@proveedor.com"

    def test_provedor_edge_cases(self):
        """Test de casos límite"""
        from src.dominio.entities.provedor import Pais, Provedor

        # Test con valores mínimos
        min_prov = Provedor(id=1, nit=1, nombre="A", pais=Pais.OTROS, direccion="A", telefono=1, email="a@a.com")

        assert min_prov.id == 1
        assert min_prov.nit == 1
        assert min_prov.nombre == "A"
        assert min_prov.telefono == 1
        assert min_prov.email == "a@a.com"

        # Test con valores grandes
        max_prov = Provedor(
            id=999999,
            nit=999999999,
            nombre="Proveedor con Nombre Muy Largo para Testing",
            pais=Pais.URUGUAY,
            direccion="Dirección muy larga con muchos detalles y especificaciones",
            telefono=9999999999,
            email="proveedor.muy.largo@dominio.extenso.com",
        )

        assert max_prov.id == 999999
        assert max_prov.nit == 999999999
        assert len(max_prov.nombre) > 20
        assert len(max_prov.direccion) > 30
        assert len(max_prov.email) > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
