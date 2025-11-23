from typing import Any, Dict

from src.aplicacion.dtos.producto_dto import ProductoDto
from src.dominio.entities.producto import Producto


class ProductoMapper:
    @staticmethod
    def json_to_dto(producto: Dict[str, Any]) -> ProductoDto:
        return ProductoDto(
            id=producto["id"],
            nombre=producto["nombre"],
            descripcion=producto["descripcion"],
            categoria=producto["categoria"],
            condiciones_almacenamiento=producto["condiciones_almacenamiento"],
            valor_unitario=producto["valor_unitario"],
            cantidad_disponible=producto["cantidad_disponible"],
            fecha_vencimiento=producto["fecha_vencimiento"],
            lote=producto["lote"],
            tiempo_estimado_entrega=producto["tiempo_estimado_entrega"],
            id_proveedor=producto["id_proveedor"],
            ubicacion=producto["ubicacion"],
        )

    @staticmethod
    def dto_to_json(producto_dto: ProductoDto) -> Dict[str, Any]:
        return {
            "id": producto_dto.id,
            "nombre": producto_dto.nombre,
            "descripcion": producto_dto.descripcion,
            "valor_unitario": producto_dto.valor_unitario,
            "categoria": producto_dto.categoria,
            "condiciones_almacenamiento": producto_dto.condiciones_almacenamiento,
            "cantidad_disponible": producto_dto.cantidad_disponible,
            "fecha_vencimiento": producto_dto.fecha_vencimiento,
            "lote": producto_dto.lote,
            "tiempo_estimado_entrega": producto_dto.tiempo_estimado_entrega,
            "id_proveedor": producto_dto.id_proveedor,
            "ubicacion": producto_dto.ubicacion,
        }

    @staticmethod
    def dto_to_entity(producto_dto: ProductoDto) -> Producto:
        return Producto(
            id=producto_dto.id,
            nombre=producto_dto.nombre,
            descripcion=producto_dto.descripcion,
            categoria=producto_dto.categoria,
            condiciones_almacenamiento=producto_dto.condiciones_almacenamiento,
            valor_unitario=producto_dto.valor_unitario,
            cantidad_disponible=producto_dto.cantidad_disponible,
            fecha_vencimiento=producto_dto.fecha_vencimiento,
            lote=producto_dto.lote,
            tiempo_estimado_entrega=producto_dto.tiempo_estimado_entrega,
            id_proveedor=producto_dto.id_proveedor,
            ubicacion=producto_dto.ubicacion,
        )

    @staticmethod
    def entity_to_dto(producto: Producto) -> ProductoDto:
        return ProductoDto(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            categoria=producto.categoria,
            condiciones_almacenamiento=producto.condiciones_almacenamiento,
            valor_unitario=float(producto.valor_unitario),
            cantidad_disponible=producto.cantidad_disponible,
            fecha_vencimiento=producto.fecha_vencimiento,
            lote=producto.lote,
            tiempo_estimado_entrega=producto.tiempo_estimado_entrega,
            id_proveedor=producto.id_proveedor,
            ubicacion=producto.ubicacion,
        )
