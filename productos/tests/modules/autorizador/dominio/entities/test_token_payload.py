"""
Tests unitarios para TokenPayload
"""

from datetime import datetime, timedelta

import pytest
from src.modules.autorizador.dominio.entities.token_payload import Role, TokenPayload


class TestRole:
    """Tests para el enum Role"""

    def test_role_values(self):
        """Test de los valores del enum Role"""
        assert Role.ADMIN.value == "ADMIN"
        assert Role.MANAGER.value == "MANAGER"
        assert Role.USER.value == "USER"
        assert Role.VIEWER.value == "VIEWER"


class TestTokenPayload:
    """Tests para TokenPayload"""

    def test_token_payload_creation(self):
        """Test de creación de TokenPayload"""
        exp = datetime.utcnow() + timedelta(hours=1)
        payload = TokenPayload(
            user_id="user-001",
            role=Role.ADMIN,
            exp=exp,
        )

        assert payload.user_id == "user-001"
        assert payload.role == Role.ADMIN
        assert payload.exp == exp
        assert payload.iat is None

    def test_token_payload_with_iat(self):
        """Test de creación de TokenPayload con iat"""
        exp = datetime.utcnow() + timedelta(hours=1)
        iat = datetime.utcnow()
        payload = TokenPayload(
            user_id="user-001",
            role=Role.USER,
            exp=exp,
            iat=iat,
        )

        assert payload.user_id == "user-001"
        assert payload.role == Role.USER
        assert payload.exp == exp
        assert payload.iat == iat

    def test_token_payload_from_dict(self):
        """Test de creación desde diccionario"""
        exp_timestamp = int((datetime.utcnow() + timedelta(hours=1)).timestamp())
        iat_timestamp = int(datetime.utcnow().timestamp())

        data = {
            "user_id": "user-001",
            "role": "ADMIN",
            "exp": exp_timestamp,
            "iat": iat_timestamp,
        }

        payload = TokenPayload.from_dict(data)

        assert payload.user_id == "user-001"
        assert payload.role == Role.ADMIN
        assert isinstance(payload.exp, datetime)
        assert isinstance(payload.iat, datetime)

    def test_token_payload_from_dict_lowercase_role(self):
        """Test de creación desde diccionario con rol en minúsculas"""
        exp_timestamp = int((datetime.utcnow() + timedelta(hours=1)).timestamp())

        data = {
            "user_id": "user-002",
            "role": "user",  # minúsculas
            "exp": exp_timestamp,
        }

        payload = TokenPayload.from_dict(data)

        assert payload.role == Role.USER

    def test_token_payload_from_dict_without_iat(self):
        """Test de creación desde diccionario sin iat"""
        exp_timestamp = int((datetime.utcnow() + timedelta(hours=1)).timestamp())

        data = {
            "user_id": "user-003",
            "role": "VIEWER",
            "exp": exp_timestamp,
        }

        payload = TokenPayload.from_dict(data)

        assert payload.user_id == "user-003"
        assert payload.role == Role.VIEWER
        assert payload.iat is None

    def test_token_payload_is_expired(self):
        """Test de verificación de expiración"""
        # Token expirado
        expired_exp = datetime.utcnow() - timedelta(hours=1)
        expired_payload = TokenPayload(
            user_id="user-001",
            role=Role.USER,
            exp=expired_exp,
        )
        assert expired_payload.is_expired() is True

        # Token no expirado
        future_exp = datetime.utcnow() + timedelta(hours=1)
        valid_payload = TokenPayload(
            user_id="user-001",
            role=Role.USER,
            exp=future_exp,
        )
        assert valid_payload.is_expired() is False

    def test_token_payload_has_role(self):
        """Test de verificación de rol"""
        payload = TokenPayload(
            user_id="user-001",
            role=Role.ADMIN,
            exp=datetime.utcnow() + timedelta(hours=1),
        )

        assert payload.has_role(Role.ADMIN) is True
        assert payload.has_role(Role.USER) is False
        assert payload.has_role(Role.VIEWER) is False

    def test_token_payload_has_admin_access(self):
        """Test de verificación de acceso de administrador"""
        admin_payload = TokenPayload(
            user_id="user-001",
            role=Role.ADMIN,
            exp=datetime.utcnow() + timedelta(hours=1),
        )
        assert admin_payload.has_admin_access() is True

        user_payload = TokenPayload(
            user_id="user-002",
            role=Role.USER,
            exp=datetime.utcnow() + timedelta(hours=1),
        )
        assert user_payload.has_admin_access() is False

        viewer_payload = TokenPayload(
            user_id="user-003",
            role=Role.VIEWER,
            exp=datetime.utcnow() + timedelta(hours=1),
        )
        assert viewer_payload.has_admin_access() is False

    def test_token_payload_different_roles(self):
        """Test de diferentes roles"""
        roles = [Role.ADMIN, Role.MANAGER, Role.USER, Role.VIEWER]

        for role in roles:
            payload = TokenPayload(
                user_id="user-001",
                role=role,
                exp=datetime.utcnow() + timedelta(hours=1),
            )
            assert payload.role == role
            assert payload.has_role(role) is True
