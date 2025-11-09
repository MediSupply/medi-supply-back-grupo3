from typing import List, Optional

from src.aplicacion.servicios.cliente_service import ClienteService
from src.dominio.entities.cliente import Cliente


class ClienteUseCase:
    """Caso de uso para clientes."""

    def __init__(self, cliente_service: ClienteService):
        self.cliente_service = cliente_service

    def obtener_todos_los_clientes(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        return self.cliente_service.obtener_todos_los_clientes()

    def obtener_cliente_por_id(self, cliente_id: str) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        return self.cliente_service.obtener_cliente_por_id(cliente_id)

    def obtener_clientes_por_categoria(self, categoria: str) -> List[Cliente]:
        """Obtiene clientes por categoría."""
        return self.cliente_service.obtener_clientes_por_categoria(categoria)

    def buscar_clientes_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre."""
        return self.cliente_service.buscar_clientes_por_nombre(nombre)

    def crear_cliente(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente."""
        return self.cliente_service.crear_cliente(cliente)
