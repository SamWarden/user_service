from collections.abc import Callable
from typing import Any

import orjson
import structlog

ProcessorType = Callable[
    [
        structlog.types.WrappedLogger, str, structlog.types.EventDict,
    ], str | bytes
]


def additionally_serialize(obj: Any) -> Any:
    raise TypeError(f"TypeError: Type is not JSON serializable: {type(obj)}")


def serialize_to_json(data: Any, default: Any) -> str:
    # print(data)
    return orjson.dumps(data, default=additionally_serialize).decode()


def get_render_processor(
    render_json_logs: bool = False,
    serializer: Callable[..., str | bytes] = serialize_to_json,
    colors: bool = True,
) -> ProcessorType:
    if render_json_logs:
        return structlog.processors.JSONRenderer(serializer=serializer)
    return structlog.dev.ConsoleRenderer(colors=colors)
