"""
Tests unitarios para TokenValidator
"""

from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import jwt

from src.modules.autorizador.aplicacion.use_cases.token_validator import TokenValidator
from src.modules.autorizador.dominio.exceptions import ExpiredTokenError, InvalidTokenError


class TestTokenValidator:
    """Tests para TokenValidator"""

    @pytest.fixture
    def secret_key(self):
        """Fixture para la clave secreta"""
        return "test-secret-key-with-at-least-32-characters-for-security"

    @pytest.fixture
    def validator(self, secret_key):
        """Fixture para crear un TokenValidator"""
        return TokenValidator(secret_key, "HS256")

    def test_token_validator_init(self, secret_key):
        """Test de inicialización de TokenValidator"""
        validator = TokenValidator(secret_key, "HS256")
        assert validator.secret_key == secret_key
        assert validator.algorithm == "HS256"

    def test_extract_token_from_header_valid(self, validator):
        """Test de extracción de token válido"""
        header = "Bearer valid.jwt.token"
        token = validator.extract_token_from_header(header)
        assert token == "valid.jwt.token"

    def test_extract_token_from_header_none(self, validator):
        """Test de extracción con header None"""
        token = validator.extract_token_from_header(None)
        assert token is None

    def test_extract_token_from_header_empty(self, validator):
        """Test de extracción con header vacío"""
        token = validator.extract_token_from_header("")
        assert token is None

    def test_extract_token_from_header_no_bearer(self, validator):
        """Test de extracción sin Bearer"""
        token = validator.extract_token_from_header("Token valid.jwt.token")
        assert token is None

    def test_extract_token_from_header_malformed(self, validator):
        """Test de extracción con header malformado"""
        with pytest.raises(InvalidTokenError):
            validator.extract_token_from_header("Bearer")

    def test_extract_token_from_header_short_token(self, validator):
        """Test de extracción con token muy corto"""
        with pytest.raises(InvalidTokenError):
            validator.extract_token_from_header("Bearer short")

    def test_extract_token_from_header_invalid_jwt_format(self, validator):
        """Test de extracción con formato JWT inválido"""
        with pytest.raises(InvalidTokenError):
            validator.extract_token_from_header("Bearer not.a.valid.jwt.token.format")

    def test_validate_token_valid(self, validator, secret_key):
        """Test de validación de token válido"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        token_payload = validator.validate_token(token)

        assert token_payload.user_id == "user-001"
        assert token_payload.role.value == "ADMIN"

    def test_validate_token_expired(self, validator, secret_key):
        """Test de validación de token expirado"""
        exp = datetime.utcnow() - timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
            "iat": datetime.utcnow() - timedelta(hours=2),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        with pytest.raises(ExpiredTokenError):
            validator.validate_token(token)

    def test_validate_token_invalid_signature(self, validator):
        """Test de validación con firma inválida"""
        other_secret = "other-secret-key-with-at-least-32-characters"
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp,
        }
        token = jwt.encode(payload, other_secret, algorithm="HS256")

        with pytest.raises(InvalidTokenError):
            validator.validate_token(token)

    def test_validate_token_empty(self, validator):
        """Test de validación con token vacío"""
        with pytest.raises(InvalidTokenError):
            validator.validate_token("")

    def test_validate_token_none(self, validator):
        """Test de validación con token None"""
        with pytest.raises(InvalidTokenError):
            validator.validate_token(None)

    def test_validate_token_missing_fields(self, validator, secret_key):
        """Test de validación con campos faltantes"""
        payload = {"user_id": "user-001"}
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        with pytest.raises(InvalidTokenError):
            validator.validate_token(token)

    def test_validate_token_invalid_role(self, validator, secret_key):
        """Test de validación con rol inválido"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "user_id": "user-001",
            "role": "INVALID_ROLE",
            "exp": exp,
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        with pytest.raises(InvalidTokenError):
            validator.validate_token(token)

    def test_validate_payload_structure_valid(self, validator):
        """Test de validación de estructura válida"""
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        }
        validator._validate_payload_structure(payload)

    def test_validate_payload_structure_missing_user_id(self, validator):
        """Test de validación con user_id faltante"""
        payload = {
            "role": "ADMIN",
            "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        }
        with pytest.raises(InvalidTokenError):
            validator._validate_payload_structure(payload)

    def test_validate_payload_structure_missing_role(self, validator):
        """Test de validación con role faltante"""
        payload = {
            "user_id": "user-001",
            "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        }
        with pytest.raises(InvalidTokenError):
            validator._validate_payload_structure(payload)

    def test_validate_payload_structure_missing_exp(self, validator):
        """Test de validación con exp faltante"""
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
        }
        with pytest.raises(InvalidTokenError):
            validator._validate_payload_structure(payload)

    def test_validate_payload_structure_invalid_user_id_type(self, validator):
        """Test de validación con tipo de user_id inválido"""
        payload = {
            "user_id": None,
            "role": "ADMIN",
            "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        }
        with pytest.raises(InvalidTokenError):
            validator._validate_payload_structure(payload)

    def test_validate_payload_structure_invalid_exp_type(self, validator):
        """Test de validación con tipo de exp inválido"""
        payload = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": "not-a-timestamp",
        }
        with pytest.raises(InvalidTokenError):
            validator._validate_payload_structure(payload)

