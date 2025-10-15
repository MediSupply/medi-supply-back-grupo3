from typing import Any, Dict

from modules.autenticador.aplicacion.dtos.user_dto import RoleDto, UserDto
from modules.autenticador.dominio.entities.user import Role, User


class UserMapper:
    @staticmethod
    def json_to_dto(user: Dict[str, Any]) -> UserDto:
        return UserDto(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            password=user["password"],
            role=RoleDto(user["role"]),
            token=user["token"],
        )

    @staticmethod
    def dto_to_json(user_dto: UserDto) -> Dict[str, Any]:
        return {
            "id": user_dto.id,
            "name": user_dto.name,
            "email": user_dto.email,
            "password": user_dto.password,
            "role": user_dto.role.value,
            "token": user_dto.token,
        }

    @staticmethod
    def dto_to_entity(user_dto: UserDto) -> User:
        # Convertir de DTO (minúsculas) a Domain (mayúsculas)
        role_value = user_dto.role.value.upper()  # "user" -> "USER", "admin" -> "ADMIN"
        role = Role(role_value)
        return User(
            id=user_dto.id,
            name=user_dto.name,
            email=user_dto.email,
            password=user_dto.password,
            role=role,
        )

    @staticmethod
    def entity_to_dto(user: User) -> UserDto:
        # Convertir de Domain (mayúsculas) a DTO (minúsculas)
        role_value = user.role.value.lower()  # "USER" -> "user", "ADMIN" -> "admin"
        role = RoleDto(role_value)
        return UserDto(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            role=role,
            token="",  # Token is not part of domain entity
        )

    @staticmethod
    def infrastructure_to_domain(infra_user) -> User:
        """Convert infrastructure User model to domain User entity"""
        from modules.autenticador.dominio.entities.user import Role as DomainRole

        # Convert infrastructure role to domain role
        domain_role = DomainRole(infra_user.role.value)

        return User(
            id=infra_user.id,
            name=infra_user.name,
            email=infra_user.email,
            password=infra_user.password,
            role=domain_role,
        )

    @staticmethod
    def domain_to_infrastructure(domain_user: User):
        """Convert domain User entity to infrastructure User model"""
        from modules.autenticador.infraestructura.dto.user import Role as InfraRole
        from modules.autenticador.infraestructura.dto.user import User as InfraUser

        # Convert domain role to infrastructure role
        infra_role = InfraRole(domain_user.role.value)

        return InfraUser(
            id=domain_user.id,
            name=domain_user.name,
            email=domain_user.email,
            password=domain_user.password,
            role=infra_role,
        )
