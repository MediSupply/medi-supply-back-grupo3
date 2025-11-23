from abc import ABC, abstractmethod
from typing import List, Optional

from src.dominio.entities.cliente import Cliente


class ClienteRepository(ABC):
    """Interfaz del repositorio de clientes."""

    @abstractmethod
    def obtener_todos(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        pass

    @abstractmethod
    def obtener_por_id(self, cliente_id: str) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        pass

    @abstractmethod
    def obtener_por_categoria(self, categoria: str) -> List[Cliente]:
        """Obtiene clientes por categoría."""
        pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre."""
        pass

    @abstractmethod
    def crear(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente."""
        pass
