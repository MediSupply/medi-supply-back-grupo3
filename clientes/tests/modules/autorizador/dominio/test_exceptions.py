"""
Tests unitarios para las excepciones del módulo de autorización
"""

import pytest

from src.modules.autorizador.dominio.exceptions import (
    AuthorizationError,
    InvalidTokenError,
    ExpiredTokenError,
    InsufficientPermissionsError,
    MissingTokenError,
)


class TestExceptions:
    """Tests para las excepciones"""

    def test_authorization_error_base(self):
        """Test de excepción base AuthorizationError"""
        error = AuthorizationError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_invalid_token_error(self):
        """Test de InvalidTokenError"""
        error = InvalidTokenError("Token inválido")
        assert str(error) == "Token inválido"
        assert isinstance(error, AuthorizationError)

    def test_invalid_token_error_default_message(self):
        """Test de InvalidTokenError con mensaje por defecto"""
        error = InvalidTokenError()
        assert str(error) == "Token inválido"
        assert isinstance(error, AuthorizationError)

    def test_expired_token_error(self):
        """Test de ExpiredTokenError"""
        error = ExpiredTokenError("Token expirado")
        assert str(error) == "Token expirado"
        assert isinstance(error, AuthorizationError)

    def test_expired_token_error_default_message(self):
        """Test de ExpiredTokenError con mensaje por defecto"""
        error = ExpiredTokenError()
        assert str(error) == "Token expirado"
        assert isinstance(error, AuthorizationError)

    def test_insufficient_permissions_error(self):
        """Test de InsufficientPermissionsError"""
        error = InsufficientPermissionsError("Permisos insuficientes")
        assert str(error) == "Permisos insuficientes"
        assert isinstance(error, AuthorizationError)

    def test_insufficient_permissions_error_default_message(self):
        """Test de InsufficientPermissionsError con mensaje por defecto"""
        error = InsufficientPermissionsError()
        assert str(error) == "Permisos insuficientes"
        assert isinstance(error, AuthorizationError)

    def test_missing_token_error(self):
        """Test de MissingTokenError"""
        error = MissingTokenError("Token requerido")
        assert str(error) == "Token requerido"
        assert isinstance(error, AuthorizationError)

    def test_missing_token_error_default_message(self):
        """Test de MissingTokenError con mensaje por defecto"""
        error = MissingTokenError()
        assert str(error) == "Token requerido"
        assert isinstance(error, AuthorizationError)

