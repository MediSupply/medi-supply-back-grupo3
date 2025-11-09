from typing import List, Optional

from src.dominio.entities.producto import Producto
from src.dominio.repositorios.producto_repository import ProductoRepository
from src.infraestructura.config.db import db_productos
from src.infraestructura.dto.producto import ProductoModel


class ProductoRepositoryImpl(ProductoRepository):
    """Implementación del repositorio de productos con base de datos SQLAlchemy."""

    def _model_to_entity(self, model: ProductoModel) -> Producto:
        """Convierte un modelo de base de datos a una entidad del dominio."""
        return Producto(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            categoria=model.categoria,
            condiciones_almacenamiento=model.condiciones_almacenamiento,
            valor_unitario=model.valor_unitario,
            cantidad_disponible=model.cantidad_disponible,
            fecha_vencimiento=model.fecha_vencimiento,
            lote=model.lote,
            tiempo_estimado_entrega=model.tiempo_estimado_entrega,
            id_proveedor=model.id_proveedor,
        )

    def _entity_to_model(self, entity: Producto) -> ProductoModel:
        """Convierte una entidad del dominio a un modelo de base de datos."""
        return ProductoModel(
            id=entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            categoria=entity.categoria,
            condiciones_almacenamiento=entity.condiciones_almacenamiento,
            valor_unitario=entity.valor_unitario,
            cantidad_disponible=entity.cantidad_disponible,
            fecha_vencimiento=entity.fecha_vencimiento,
            lote=entity.lote,
            tiempo_estimado_entrega=entity.tiempo_estimado_entrega,
            id_proveedor=entity.id_proveedor,
        )

    def obtener_todos(self) -> List[Producto]:
        """Obtiene todos los productos."""
        try:
            models = db_productos.session.query(ProductoModel).all()
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            print(f"Error obteniendo todos los productos: {e}")
            return []

    def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        try:
            model = db_productos.session.query(ProductoModel).filter_by(id=producto_id).first()
            if model:
                return self._model_to_entity(model)
            return None
        except Exception as e:
            print(f"Error obteniendo producto por ID: {e}")
            return None

    def obtener_por_categoria(self, categoria: str) -> List[Producto]:
        """Obtiene productos por categoría."""
        try:
            models = db_productos.session.query(ProductoModel).filter_by(categoria=categoria).all()
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            print(f"Error obteniendo productos por categoría: {e}")
            return []

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre."""
        try:
            models = (
                db_productos.session.query(ProductoModel)
                .filter(ProductoModel.nombre.ilike(f"%{nombre}%"))
                .all()
            )
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            print(f"Error buscando productos por nombre: {e}")
            return []
