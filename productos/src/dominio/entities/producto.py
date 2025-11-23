from dataclasses import dataclass
import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class Producto:
    """
    Entidad del dominio que representa un producto.
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

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "condiciones_almacenamiento": self.condiciones_almacenamiento,
            "valor_unitario": float(self.valor_unitario),
            "cantidad_disponible": self.cantidad_disponible,
            "fecha_vencimiento": self.fecha_vencimiento,
            "lote": self.lote,
            "tiempo_estimado_entrega": self.tiempo_estimado_entrega,
            "id_proveedor": self.id_proveedor,
            "ubicacion": self.ubicacion,
        }
