from flask import Blueprint, request
from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd


def create_auth_routes(auth_controller: AuthCmd) -> Blueprint:
    """
    Crea y configura las rutas relacionadas con autenticación.

    Args:
        auth_controller: Instancia del controlador de autenticación

    Returns:
        Blueprint: Blueprint de Flask con las rutas configuradas
    """
    auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

    @auth_bp.route("/login", methods=["POST"])
    def login():
        """Endpoint para iniciar sesión."""
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        return auth_controller.login(email, password)

    @auth_bp.route("/signup", methods=["POST"])
    def signup():
        """Endpoint para registrarse."""
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "USER")
        return auth_controller.signUp(name, email, password, role)

    @auth_bp.route("/signout", methods=["POST"])
    def signout():
        """Endpoint para cerrar sesión."""
        return auth_controller.signOut()

    @auth_bp.route("/me", methods=["GET"])
    def get_me():
        """Endpoint para obtener información del usuario autenticado."""
        return auth_controller.get_me()

    return auth_bp
