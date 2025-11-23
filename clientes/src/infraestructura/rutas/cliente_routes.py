from flask import Blueprint, request
from src.infraestructura.cmd.cliente_cmd import ClienteCmd


def create_cliente_routes(cliente_controller: ClienteCmd) -> Blueprint:
    """Crea las rutas para clientes."""

    cliente_routes = Blueprint("clientes", __name__, url_prefix="/clientes")

    @cliente_routes.route("", methods=["GET"])
    def obtener_todos_los_clientes():
        """Obtiene todos los clientes."""
        return cliente_controller.obtener_todos_los_clientes()

    @cliente_routes.route("/<string:cliente_id>", methods=["GET"])
    def obtener_cliente_por_id(cliente_id: str):
        """Obtiene un cliente por su ID."""
        return cliente_controller.obtener_cliente_por_id(cliente_id)

    @cliente_routes.route("/categoria/<string:categoria>", methods=["GET"])
    def obtener_clientes_por_categoria(categoria: str):
        """Obtiene clientes por categoría."""
        return cliente_controller.obtener_clientes_por_categoria(categoria)

    @cliente_routes.route("/buscar", methods=["GET"])
    def buscar_clientes_por_nombre():
        """Busca clientes por nombre."""
        nombre = request.args.get("nombre", "")
        if not nombre:
            return {"error": "Parámetro nombre es requerido"}, 400

        return cliente_controller.buscar_clientes_por_nombre(nombre)

    @cliente_routes.route("", methods=["POST"])
    def crear_cliente():
        """Crea un nuevo cliente."""
        data = request.get_json()
        if not data:
            return {"error": "Cuerpo de la petición requerido"}, 400

        return cliente_controller.crear_cliente(data)

    return cliente_routes
