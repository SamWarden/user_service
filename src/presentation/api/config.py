import tomllib
from dataclasses import dataclass

from dataclass_factory import Factory

from src.infrastructure.log import LoggingConfig


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


@dataclass
class Config:
    logging: LoggingConfig


def load_config(path: str) -> Config:
    data = read_toml(path)

    dcf = Factory()
    config = dcf.load(data, Config)
    return config
