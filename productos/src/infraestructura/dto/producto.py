from datetime import datetime

from src.infraestructura.config.db import db_productos


class ProductoModel(db_productos.Model):
    """Modelo de base de datos para Producto."""

    __tablename__ = "productos"

    id = db_productos.Column(db_productos.String, nullable=False, primary_key=True)
    nombre = db_productos.Column(db_productos.String, nullable=False)
    descripcion = db_productos.Column(db_productos.String, nullable=False)
    categoria = db_productos.Column(db_productos.String, nullable=False)
    condiciones_almacenamiento = db_productos.Column(db_productos.String, nullable=False)
    valor_unitario = db_productos.Column(db_productos.Float, nullable=False)
    cantidad_disponible = db_productos.Column(db_productos.Integer, nullable=False)
    fecha_vencimiento = db_productos.Column(db_productos.DateTime, nullable=False)
    lote = db_productos.Column(db_productos.String, nullable=False)
    tiempo_estimado_entrega = db_productos.Column(db_productos.String, nullable=False)
    id_proveedor = db_productos.Column(db_productos.String, nullable=False)
    ubicacion = db_productos.Column(db_productos.String, nullable=False)

    def __repr__(self):
        return f"<ProductoModel {self.id}: {self.nombre}>"
