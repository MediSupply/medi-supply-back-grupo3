"""
Tests unitarios para las excepciones del módulo de autorización
"""

import pytest

from src.modules.autorizador.dominio.exceptions import (
    AuthorizationError,
    ExpiredTokenError,
    InsufficientPermissionsError,
    InvalidTokenError,
    MissingTokenError,
)


class TestExceptions:
    """Tests para las excepciones de autorización"""

    def test_authorization_error_base(self):
        """Test de la excepción base AuthorizationError"""
        error = AuthorizationError("Error de autorización")
        assert isinstance(error, Exception)
        assert str(error) == "Error de autorización"

    def test_invalid_token_error(self):
        """Test de InvalidTokenError"""
        error = InvalidTokenError("Token inválido")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token inválido"

    def test_invalid_token_error_default_message(self):
        """Test de InvalidTokenError con mensaje por defecto"""
        error = InvalidTokenError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token inválido"

    def test_expired_token_error(self):
        """Test de ExpiredTokenError"""
        error = ExpiredTokenError("Token expirado")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token expirado"

    def test_expired_token_error_default_message(self):
        """Test de ExpiredTokenError con mensaje por defecto"""
        error = ExpiredTokenError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token expirado"

    def test_insufficient_permissions_error(self):
        """Test de InsufficientPermissionsError"""
        error = InsufficientPermissionsError("Permisos insuficientes")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Permisos insuficientes"

    def test_insufficient_permissions_error_default_message(self):
        """Test de InsufficientPermissionsError con mensaje por defecto"""
        error = InsufficientPermissionsError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Permisos insuficientes"

    def test_missing_token_error(self):
        """Test de MissingTokenError"""
        error = MissingTokenError("Token requerido")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token requerido"

    def test_missing_token_error_default_message(self):
        """Test de MissingTokenError con mensaje por defecto"""
        error = MissingTokenError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token requerido"

    def test_exception_inheritance(self):
        """Test de que todas las excepciones heredan de AuthorizationError"""
        assert issubclass(InvalidTokenError, AuthorizationError)
        assert issubclass(ExpiredTokenError, AuthorizationError)
        assert issubclass(InsufficientPermissionsError, AuthorizationError)
        assert issubclass(MissingTokenError, AuthorizationError)

