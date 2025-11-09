"""
Tests unitarios para ProductoMapper
"""

from datetime import datetime
import pytest

from src.aplicacion.mappers.producto_mapper import ProductoMapper
from src.dominio.entities.producto import Producto
from src.aplicacion.dtos.producto_dto import ProductoDto


class TestProductoMapper:
    """Tests para ProductoMapper"""

    def test_json_to_dto(self):
        """Test de conversión de JSON a DTO"""
        json_data = {
            "id": "prod-001",
            "nombre": "Laptop",
            "descripcion": "Laptop gaming",
            "categoria": "electronicos",
            "condiciones_almacenamiento": "Temperatura ambiente",
            "valor_unitario": 1500.00,
            "cantidad_disponible": 10,
            "fecha_vencimiento": datetime(2025, 12, 31),
            "lote": "LOT-001",
            "tiempo_estimado_entrega": "5 días",
            "id_proveedor": "prov-001",
        }

        dto = ProductoMapper.json_to_dto(json_data)

        assert isinstance(dto, ProductoDto)
        assert dto.id == "prod-001"
        assert dto.nombre == "Laptop"
        assert dto.valor_unitario == 1500.00
        assert dto.cantidad_disponible == 10

    def test_dto_to_json(self, sample_producto_dto):
        """Test de conversión de DTO a JSON"""
        json_data = ProductoMapper.dto_to_json(sample_producto_dto)

        assert isinstance(json_data, dict)
        assert json_data["id"] == "prod-001"
        assert json_data["nombre"] == "Laptop"
        assert json_data["valor_unitario"] == 1500.00
        assert json_data["categoria"] == "electronicos"
        assert json_data["cantidad_disponible"] == 10
        assert json_data["lote"] == "LOT-001"
        assert json_data["tiempo_estimado_entrega"] == "5 días"
        assert json_data["id_proveedor"] == "prov-001"

    def test_dto_to_entity(self, sample_producto_dto):
        """Test de conversión de DTO a Entity"""
        entity = ProductoMapper.dto_to_entity(sample_producto_dto)

        assert isinstance(entity, Producto)
        assert entity.id == "prod-001"
        assert entity.nombre == "Laptop"
        assert entity.valor_unitario == 1500.00
        assert entity.cantidad_disponible == 10
        assert entity.categoria == "electronicos"
        assert entity.lote == "LOT-001"

    def test_entity_to_dto(self, sample_producto):
        """Test de conversión de Entity a DTO"""
        dto = ProductoMapper.entity_to_dto(sample_producto)

        assert isinstance(dto, ProductoDto)
        assert dto.id == "prod-001"
        assert dto.nombre == "Laptop"
        assert dto.valor_unitario == 1500.00
        assert dto.cantidad_disponible == 10
        assert dto.categoria == "electronicos"
        assert dto.lote == "LOT-001"

    def test_round_trip_entity_dto(self, sample_producto):
        """Test de ida y vuelta: Entity -> DTO -> Entity"""
        dto = ProductoMapper.entity_to_dto(sample_producto)
        entity = ProductoMapper.dto_to_entity(dto)

        assert entity.id == sample_producto.id
        assert entity.nombre == sample_producto.nombre
        assert entity.valor_unitario == sample_producto.valor_unitario
        assert entity.cantidad_disponible == sample_producto.cantidad_disponible

    def test_round_trip_dto_json(self, sample_producto_dto):
        """Test de ida y vuelta: DTO -> JSON -> DTO"""
        json_data = ProductoMapper.dto_to_json(sample_producto_dto)
        dto = ProductoMapper.json_to_dto(json_data)

        assert dto.id == sample_producto_dto.id
        assert dto.nombre == sample_producto_dto.nombre
        assert dto.valor_unitario == sample_producto_dto.valor_unitario
        assert dto.cantidad_disponible == sample_producto_dto.cantidad_disponible

    def test_mapper_with_different_values(self):
        """Test del mapper con diferentes valores"""
        producto = Producto(
            id="prod-999",
            nombre="Producto Test",
            descripcion="Descripción test",
            categoria="deportes",
            condiciones_almacenamiento="Frío",
            valor_unitario=99.99,
            cantidad_disponible=5,
            fecha_vencimiento=datetime(2026, 1, 1),
            lote="LOT-999",
            tiempo_estimado_entrega="1 día",
            id_proveedor="prov-999",
        )

        dto = ProductoMapper.entity_to_dto(producto)
        assert dto.id == "prod-999"
        assert dto.categoria == "deportes"
        assert dto.valor_unitario == 99.99

        json_data = ProductoMapper.dto_to_json(dto)
        assert json_data["id"] == "prod-999"
        assert json_data["categoria"] == "deportes"

