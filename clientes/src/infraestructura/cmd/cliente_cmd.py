from typing import List, Optional

from flask import jsonify
from src.aplicacion.mappers.cliente_mapper import ClienteMapper
from src.aplicacion.use_cases.cliente_use_case import ClienteUseCase
from src.dominio.entities.cliente import Cliente


class ClienteCmd:
    """Controlador para clientes."""

    def __init__(self, cliente_use_case: ClienteUseCase):
        self.cliente_use_case = cliente_use_case

    def obtener_todos_los_clientes(self):
        """Obtiene todos los clientes."""
        try:
            clientes = self.cliente_use_case.obtener_todos_los_clientes()
            clientes_dto = [ClienteMapper.entity_to_dto(c) for c in clientes]
            clientes_json = [ClienteMapper.dto_to_json(c) for c in clientes_dto]

            return jsonify( clientes_json), 200
        except Exception as e:
            return jsonify({ "error": str(e)}), 500

    def obtener_cliente_por_id(self, cliente_id: str):
        """Obtiene un producto por su ID."""
        try:
            cliente = self.cliente_use_case.obtener_cliente_por_id(cliente_id)
            if not cliente:
                return jsonify({ "error": "Cliente no encontrado"}), 404

            cliente_dto = ClienteMapper.entity_to_dto(cliente)
            cliente_json = ClienteMapper.dto_to_json(cliente_dto)

            return jsonify( cliente_json), 200
        except Exception as e:
            return jsonify({ "error": str(e)}), 500

    def obtener_clientes_por_categoria(self, categoria: str):
        """Obtiene clientes por categoría."""
        try:
            clientes = self.cliente_use_case.obtener_clientes_por_categoria(categoria)
            clientes_dto = [ClienteMapper.entity_to_dto(c) for c in clientes]
            clientes_json = [ClienteMapper.dto_to_json(c) for c in clientes_dto]

            return (
                jsonify( clientes_json),
                200,
            )
        except Exception as e:
            return jsonify({ "error": str(e)}), 500

    def buscar_clientes_por_nombre(self, nombre: str):
        """Busca clientes por nombre."""
        try:
            clientes = self.cliente_use_case.buscar_clientes_por_nombre(nombre)
            clientes_dto = [ClienteMapper.entity_to_dto(c) for c in clientes]
            clientes_json = [ClienteMapper.dto_to_json(c) for c in clientes_dto]

            return jsonify( clientes_json), 200
        except Exception as e:
            return jsonify({ "error": str(e)}), 500

    def crear_cliente(self, cliente_data: dict):
        """Crea un nuevo cliente."""
        try:
            # Convertir JSON a DTO (el mapper generará el ID si no existe)
            cliente_dto = ClienteMapper.json_to_dto(cliente_data)
            # Convertir DTO a entidad
            cliente = ClienteMapper.dto_to_entity(cliente_dto)
            # Crear el cliente
            cliente_creado = self.cliente_use_case.crear_cliente(cliente)
            # Convertir a DTO y luego a JSON para la respuesta
            cliente_dto = ClienteMapper.entity_to_dto(cliente_creado)
            cliente_json = ClienteMapper.dto_to_json(cliente_dto)

            return jsonify( cliente_json), 201
        except KeyError as e:
            return jsonify({ "error": f"Campo requerido faltante: {str(e)}"}), 400
        except Exception as e:
            return jsonify({ "error": str(e)}), 500
