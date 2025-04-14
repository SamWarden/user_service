from dataclasses import dataclass, field

from user_service.infrastructure.db import DBConfig
from user_service.infrastructure.log import LoggingConfig
from user_service.infrastructure.message_broker.config import EventBusConfig


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 5000
    debug: bool = __debug__


@dataclass
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    api: APIConfig = field(default_factory=APIConfig)
    event_bus: EventBusConfig = field(default_factory=EventBusConfig)
