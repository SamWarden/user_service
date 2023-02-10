from dataclasses import dataclass


@dataclass(frozen=True)
class EventBusConfig:
    rabbitmq_uri: str
