import tomllib
from dataclasses import dataclass

from dataclass_factory import Retort

from src.infrastructure.db import DBConfig
from src.infrastructure.log import LoggingConfig


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


@dataclass
class Config:
    db: DBConfig
    logging: LoggingConfig


def load_config(path: str) -> Config:
    data = read_toml(path)

    dcf = Retort()
    config = dcf.load(data, Config)
    return config
