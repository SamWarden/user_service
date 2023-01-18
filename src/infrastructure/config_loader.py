import tomllib
from typing import Type, TypeVar

from dataclass_factory import Retort

from src.infrastructure.constants import CONFIG_PATH

T = TypeVar("T")


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_config(config_type: Type[T], config_scope: str | None = None, path: str = CONFIG_PATH) -> T:
    data = read_toml(path)

    if config_scope is not None:
        data = data[config_scope]

    dcf = Retort()
    config = dcf.load(data, config_type)
    return config
