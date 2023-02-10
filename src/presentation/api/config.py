from dataclasses import dataclass, field

from di import bind_by_type
from di.dependent import Dependent
from didiator.utils.di_builder import DiBuilder

from src.infrastructure.constants import APP_SCOPE
from src.infrastructure.db import DBConfig
from src.infrastructure.log import LoggingConfig
from src.infrastructure.message_broker.config import EventBusConfig


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 5000


@dataclass
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    api: APIConfig = field(default_factory=APIConfig)
    event_bus: EventBusConfig = field(default_factory=EventBusConfig)


def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope=APP_SCOPE), Config))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=APP_SCOPE), DBConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.logging, scope=APP_SCOPE), LoggingConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=APP_SCOPE), APIConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.event_bus, scope=APP_SCOPE), EventBusConfig))
