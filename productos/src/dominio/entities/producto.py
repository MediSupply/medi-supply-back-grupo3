from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Dict


class Categoria(Enum):
    ELECTRONICOS = "electronicos"
    ROPA = "ropa"
    HOGAR = "hogar"
    DEPORTES = "deportes"
    LIBROS = "libros"
    OTROS = "otros"


@dataclass(frozen=True)
class Producto:
    """
    Entidad del dominio que representa un producto.
    """

    id: str
    nombre: str
    descripcion: str
    precio: Decimal
    categoria: Categoria
    stock: int
    activo: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "categoria": self.categoria.value,
            "stock": self.stock,
            "activo": self.activo,
        }
