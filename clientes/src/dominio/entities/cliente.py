from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Cliente:
    """
    Entidad del dominio que representa un cliente.
    """

    id: str
    nombre: str
    email: str
    telefono: str
    direccion: str
    razon_social: str
    nit: str

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "razon_social": self.razon_social,
            "nit": self.nit,
        }
