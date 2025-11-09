import os

import requests
from flask import Blueprint, current_app, jsonify, request


def create_cliente_routes() -> Blueprint:
    """
    Crea las rutas para clientes que hacen proxy al microservicio.
    """

    cliente_routes = Blueprint("clientes", __name__, url_prefix="/clientes")

    def get_clientes_service_url():
        """Obtiene la URL del servicio de clientes desde la configuración."""
        try:
            return current_app.config.get("CLIENTES_SERVICE_URL", os.environ.get("CLIENTES_SERVICE_URL", "http://clientes:5004"))
        except RuntimeError:
            # Si no hay contexto de aplicación, usar variable de entorno
            return os.environ.get("CLIENTES_SERVICE_URL", "http://clientes:5004")

    def make_request_to_clientes(endpoint, method="GET", params=None, data=None, headers=None):
        """Hace una petición al microservicio de clientes."""
        try:
            service_url = get_clientes_service_url()
            url = f"{service_url}{endpoint}"
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                return jsonify({"error": "Método no soportado"}), 405

            return response.json(), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({"success": False, "error": f"Error conectando con el servicio de clientes: {str(e)}"}), 503

    @cliente_routes.route("", methods=["GET"])
    def obtener_todos_los_clientes():
        """Obtiene todos los clientes."""
        headers = request.headers
        return make_request_to_clientes("/clientes", headers=headers)

    @cliente_routes.route("", methods=["POST"])
    def crear_cliente():
        """Crea un nuevo cliente."""
        headers = request.headers
        data = request.get_json()
        return make_request_to_clientes("/clientes", method="POST", headers=headers, data=data)

    @cliente_routes.route("/<string:cliente_id>", methods=["GET"])
    def obtener_cliente_por_id(cliente_id: str):
        """Obtiene un cliente por su ID."""
        headers = request.headers
        return make_request_to_clientes(f"/clientes/{cliente_id}", headers=headers)

    @cliente_routes.route("/buscar", methods=["GET"])
    def buscar_clientes_por_nombre():
        """Busca clientes por nombre."""
        headers = request.headers
        nombre = request.args.get("nombre", "")
        params = {"nombre": nombre} if nombre else None
        return make_request_to_clientes("/clientes/buscar", headers=headers, params=params)

    return cliente_routes
