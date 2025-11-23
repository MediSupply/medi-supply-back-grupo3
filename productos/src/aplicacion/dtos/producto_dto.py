from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class ProductoDto:
    """
    DTO que representa un producto.
    """

    id: str
    nombre: str
    descripcion: str
    categoria: str
    condiciones_almacenamiento: str
    valor_unitario: float
    cantidad_disponible: int
    fecha_vencimiento: datetime
    lote: str
    tiempo_estimado_entrega: str
    id_proveedor: str
    ubicacion: str
