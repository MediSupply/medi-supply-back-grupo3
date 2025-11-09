import uuid
from typing import Any, Dict

from src.aplicacion.dtos.cliente_dto import ClienteDto
from src.dominio.entities.cliente import Cliente
    

class ClienteMapper:
    @staticmethod
    def json_to_dto(cliente: Dict[str, Any]) -> ClienteDto:
        # Generar ID si no se proporciona
        cliente_id = cliente.get("id") or str(uuid.uuid4())
        return ClienteDto(
            id=cliente_id,
            nombre=cliente["nombre"],
            email=cliente["email"],
            telefono=cliente["telefono"],
            direccion=cliente["direccion"],
            razon_social=cliente["razon_social"],
            nit=cliente["nit"],
        )

    @staticmethod
    def dto_to_json(cliente_dto: ClienteDto) -> Dict[str, Any]:
        return {
            "id": cliente_dto.id,
            "nombre": cliente_dto.nombre,
            "email": cliente_dto.email,
            "telefono": cliente_dto.telefono,
            "direccion": cliente_dto.direccion,
            "razon_social": cliente_dto.razon_social,
            "nit": cliente_dto.nit,
        }

    @staticmethod
    def dto_to_entity(cliente_dto: ClienteDto) -> Cliente:
        return Cliente(
            id=cliente_dto.id,
            nombre=cliente_dto.nombre,
            email=cliente_dto.email,
            telefono=cliente_dto.telefono,
            direccion=cliente_dto.direccion,
            razon_social=cliente_dto.razon_social,
            nit=cliente_dto.nit,
        )

    @staticmethod
    def entity_to_dto(cliente: Cliente) -> ClienteDto:
        return ClienteDto(
            id=cliente.id,
            nombre=cliente.nombre,
            email=cliente.email,
            telefono=cliente.telefono,
            direccion=cliente.direccion,
            razon_social=cliente.razon_social,
            nit=cliente.nit,
        )
