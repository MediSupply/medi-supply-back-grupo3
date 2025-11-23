from dataclasses import dataclass


@dataclass(frozen=True)
class ClienteDto:
    """
    DTO que representa un cliente.
    """

    id: str
    nombre: str
    email: str
    telefono: str
    direccion: str
    razon_social: str
    nit: str
