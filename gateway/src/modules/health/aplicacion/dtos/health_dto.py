from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HealthDto:
    """
    DTO que representa el estado de salud.
    """

    status: str
    timestamp: datetime
    version: str
