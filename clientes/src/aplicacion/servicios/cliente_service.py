from typing import List, Optional

from src.dominio.entities.cliente import Cliente
from src.dominio.repositorios.cliente_repository import ClienteRepository


class ClienteService:
    """Servicio de dominio para clientes."""

    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def obtener_todos_los_clientes(self) -> List[Cliente]:
        """Obtiene todos los clientes activos."""
        clientes = self.cliente_repository.obtener_todos()
        return [c for c in clientes]

    def obtener_cliente_por_id(self, cliente_id: str) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        return self.cliente_repository.obtener_por_id(cliente_id)

    def obtener_clientes_por_categoria(self, categoria: str) -> List[Cliente]:
        """Obtiene clientes por categoría."""
        try:
            clientes = self.cliente_repository.obtener_por_categoria(categoria)
            return [c for c in clientes]
        except ValueError:
            return []

    def buscar_clientes_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre."""
        clientes = self.cliente_repository.buscar_por_nombre(nombre)
        return [c for c in clientes]

    def crear_cliente(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente."""
        return self.cliente_repository.crear(cliente)
