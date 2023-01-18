from dataclasses import dataclass

from di.container import bind_by_type
from di.dependent import Dependent
from didiator.utils.di_builder import DiBuilder

from src.infrastructure.constants import APP_SCOPE
from src.infrastructure.db import DBConfig
from src.infrastructure.log import LoggingConfig


@dataclass
class APIConfig:
    host: str = "localhost"
    port: int = 5000


@dataclass
class Config:
    db: DBConfig
    logging: LoggingConfig
    api: APIConfig


def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope=APP_SCOPE), Config))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=APP_SCOPE), DBConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.logging, scope=APP_SCOPE), LoggingConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=APP_SCOPE), APIConfig))
