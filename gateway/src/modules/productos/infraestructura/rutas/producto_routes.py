import logging
import os

import requests
from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)


def create_producto_routes() -> Blueprint:
    """
    Crea las rutas para productos que hacen proxy al microservicio.
    """

    producto_routes = Blueprint("productos", __name__, url_prefix="/productos")

    PRODUCTOS_SERVICE_URL = os.environ.get("PRODUCTOS_SERVICE_URL", "http://localhost:5002")

    def make_request_to_productos(endpoint, method="GET", params=None, data=None, headers=None):
        """Hace una petición al microservicio de productos."""
        try:
            url = f"{PRODUCTOS_SERVICE_URL}{endpoint}"
            
            # Preparar headers: convertir a diccionario y asegurar Authorization
            headers_dict = {}
            
            # Si se pasaron headers, convertirlos a dict
            if headers:
                if isinstance(headers, dict):
                    headers_dict = headers.copy()
                else:
                    # Convertir EnvironHeaders u otro tipo a dict
                    headers_dict = dict(headers)
            
            # Asegurar que el header Authorization se pase correctamente desde la request original
            auth_header = request.headers.get("Authorization")
            if auth_header:
                headers_dict["Authorization"] = auth_header
                logger.debug(f"Forwarding Authorization header to productos service")
            else:
                logger.warning(f"No Authorization header found in request to {endpoint}")
            
            logger.debug(f"Making {method} request to {url} with headers: {list(headers_dict.keys())}")
            
            if method == "GET":
                response = requests.get(url, headers=headers_dict, params=params, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=headers_dict, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=headers_dict, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers_dict, timeout=30)
            else:
                return jsonify({"error": "Método no soportado"}), 405

            logger.debug(f"Response from productos service: {response.status_code}")
            return response.json(), response.status_code

        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to productos service: {str(e)}")
            return jsonify({"success": False, "error": f"Error conectando con el servicio de productos: {str(e)}"}), 503

    @producto_routes.route("", methods=["GET"])
    def obtener_todos_los_productos():
        """Obtiene todos los productos."""
        # Preparar headers con Authorization si existe
        headers = {}
        auth_header = request.headers.get("Authorization")
        if auth_header:
            headers["Authorization"] = auth_header
        return make_request_to_productos("/productos", headers=headers)

    @producto_routes.route("/<string:producto_id>", methods=["GET"])
    def obtener_producto_por_id(producto_id: str):
        """Obtiene un producto por su ID."""
        # Preparar headers con Authorization si existe
        headers = {}
        auth_header = request.headers.get("Authorization")
        if auth_header:
            headers["Authorization"] = auth_header
        return make_request_to_productos(f"/productos/{producto_id}", headers=headers)

    return producto_routes
