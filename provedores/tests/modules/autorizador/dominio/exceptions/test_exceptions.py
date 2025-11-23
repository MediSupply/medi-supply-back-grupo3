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


class TestAuthorizationError:
    """Tests para AuthorizationError"""

    def test_authorization_error_base(self):
        """Test de la excepción base"""
        error = AuthorizationError("Error de autorización")
        assert isinstance(error, Exception)
        assert str(error) == "Error de autorización"


class TestInvalidTokenError:
    """Tests para InvalidTokenError"""

    def test_invalid_token_error_default(self):
        """Test de InvalidTokenError con mensaje por defecto"""
        error = InvalidTokenError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token inválido"

    def test_invalid_token_error_custom(self):
        """Test de InvalidTokenError con mensaje personalizado"""
        error = InvalidTokenError("Token ha sido alterado")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token ha sido alterado"

    def test_invalid_token_error_raise(self):
        """Test de que InvalidTokenError se puede lanzar"""
        with pytest.raises(InvalidTokenError) as exc_info:
            raise InvalidTokenError("Token inválido")
        assert str(exc_info.value) == "Token inválido"


class TestExpiredTokenError:
    """Tests para ExpiredTokenError"""

    def test_expired_token_error_default(self):
        """Test de ExpiredTokenError con mensaje por defecto"""
        error = ExpiredTokenError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token expirado"

    def test_expired_token_error_custom(self):
        """Test de ExpiredTokenError con mensaje personalizado"""
        error = ExpiredTokenError("El token expiró hace 5 minutos")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "El token expiró hace 5 minutos"

    def test_expired_token_error_raise(self):
        """Test de que ExpiredTokenError se puede lanzar"""
        with pytest.raises(ExpiredTokenError) as exc_info:
            raise ExpiredTokenError("Token expirado")
        assert str(exc_info.value) == "Token expirado"


class TestInsufficientPermissionsError:
    """Tests para InsufficientPermissionsError"""

    def test_insufficient_permissions_error_default(self):
        """Test de InsufficientPermissionsError con mensaje por defecto"""
        error = InsufficientPermissionsError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Permisos insuficientes"

    def test_insufficient_permissions_error_custom(self):
        """Test de InsufficientPermissionsError con mensaje personalizado"""
        error = InsufficientPermissionsError("Usuario no puede realizar esta acción")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Usuario no puede realizar esta acción"

    def test_insufficient_permissions_error_raise(self):
        """Test de que InsufficientPermissionsError se puede lanzar"""
        with pytest.raises(InsufficientPermissionsError) as exc_info:
            raise InsufficientPermissionsError("Permisos insuficientes")
        assert str(exc_info.value) == "Permisos insuficientes"


class TestMissingTokenError:
    """Tests para MissingTokenError"""

    def test_missing_token_error_default(self):
        """Test de MissingTokenError con mensaje por defecto"""
        error = MissingTokenError()
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Token requerido"

    def test_missing_token_error_custom(self):
        """Test de MissingTokenError con mensaje personalizado"""
        error = MissingTokenError("Header Authorization no encontrado")
        assert isinstance(error, AuthorizationError)
        assert str(error) == "Header Authorization no encontrado"

    def test_missing_token_error_raise(self):
        """Test de que MissingTokenError se puede lanzar"""
        with pytest.raises(MissingTokenError) as exc_info:
            raise MissingTokenError("Token requerido")
        assert str(exc_info.value) == "Token requerido"


class TestExceptionHierarchy:
    """Tests para verificar la jerarquía de excepciones"""

    def test_all_exceptions_inherit_from_authorization_error(self):
        """Test de que todas las excepciones heredan de AuthorizationError"""
        assert issubclass(InvalidTokenError, AuthorizationError)
        assert issubclass(ExpiredTokenError, AuthorizationError)
        assert issubclass(InsufficientPermissionsError, AuthorizationError)
        assert issubclass(MissingTokenError, AuthorizationError)

    def test_all_exceptions_inherit_from_exception(self):
        """Test de que todas las excepciones heredan de Exception"""
        assert issubclass(AuthorizationError, Exception)
        assert issubclass(InvalidTokenError, Exception)
        assert issubclass(ExpiredTokenError, Exception)
        assert issubclass(InsufficientPermissionsError, Exception)
        assert issubclass(MissingTokenError, Exception)

