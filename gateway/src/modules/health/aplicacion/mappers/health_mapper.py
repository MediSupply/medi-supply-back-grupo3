from datetime import datetime
from typing import Any, Dict

from modules.health.aplicacion.dtos.health_dto import HealthDto
from modules.health.dominio.entities.health import Health


class HealthMapper:
    @staticmethod
    def json_to_dto(health: Dict[str, Any]) -> HealthDto:
        return HealthDto(
            status=health["status"],
            timestamp=datetime.fromisoformat(health["timestamp"]),
            version=health["version"],
        )

    @staticmethod
    def dto_to_json(health_dto: HealthDto) -> Dict[str, Any]:
        return {
            "status": health_dto.status,
            "timestamp": health_dto.timestamp.isoformat(),
            "version": health_dto.version,
        }

    @staticmethod
    def dto_to_entity(health_dto: HealthDto) -> Health:
        return Health(
            status=health_dto.status,
            timestamp=health_dto.timestamp,
            version=health_dto.version,
        )

    @staticmethod
    def entity_to_dto(health: Health) -> HealthDto:
        return HealthDto(
            status=health.status,
            timestamp=health.timestamp,
            version=health.version,
        )
