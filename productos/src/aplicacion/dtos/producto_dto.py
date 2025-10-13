from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class CategoriaDto(Enum):
    ELECTRONICOS = "electronicos"
    ROPA = "ropa"
    HOGAR = "hogar"
    DEPORTES = "deportes"
    LIBROS = "libros"
    OTROS = "otros"


@dataclass(frozen=True)
class ProductoDto:
    """
    DTO que representa un producto.
    """

    id: str
    nombre: str
    descripcion: str
    precio: float
    categoria: CategoriaDto
    stock: int
    activo: bool = True
