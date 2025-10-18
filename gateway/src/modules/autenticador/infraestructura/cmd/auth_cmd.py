from flask import Response, jsonify
from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper
from modules.autenticador.aplicacion.use_cases.auth_use_case import AuthUseCase


class AuthCmd:
    def __init__(self, auth_use_case: AuthUseCase):
        self.auth_use_case = auth_use_case

    def login(self, email: str, password: str) -> Response:
        try:
            login_result = self.auth_use_case.execute(email, password)
            
            # Usuario no encontrado
            if login_result.user_not_found:
                return jsonify({"error": "Usuario no encontrado"}), 404
            
            # Credenciales incorrectas
            if login_result.invalid_credentials:
                return jsonify({"error": "Credenciales inválidas"}), 401
            
            # Login exitoso
            if login_result.session:
                return jsonify(SessionMapper.dto_to_json(login_result.session)), 200
            else:
                return jsonify({"error": "Error al iniciar sesión"}), 500
                
        except Exception as e:
            return jsonify({"error": "Error al iniciar sesión"}), 500

    def signUp(self, name: str, email: str, password: str, role: str = "USER") -> Response:
        try:
            # Verificar si el usuario ya existe
            if self.auth_use_case.user_exists(email):
                return jsonify({"error": f"El correo {email} ya está registrado"}), 409
            
            # Proceder con el registro
            session = self.auth_use_case.signUp(name, email, password, role)
            if session:
                return jsonify(SessionMapper.dto_to_json(session)), 201
            else:
                return jsonify({"error": "Error al registrarse"}), 500
        except Exception as e:
            return jsonify({"error": "Error al registrarse"}), 500

    def signOut(self) -> Response:
        try:
            session = self.auth_use_case.signOut()
            return jsonify({"message": "Sesión cerrada exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": "Error al cerrar sesión"}), 500
