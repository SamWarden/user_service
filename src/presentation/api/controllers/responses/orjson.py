import logging
from typing import Any
from uuid import UUID

import orjson
import pydantic
from fastapi.responses import ORJSONResponse as _ORJSONResponse

logger = logging.getLogger(__name__)


def additionally_serialize(obj: Any) -> Any:
    match obj:  # noqa: E999
        case Exception():
            text = obj.args[0] if len(obj.args) > 0 else "Unknown error"
            return f"{obj.__class__.__name__}: {text}"
        case UUID():
            return str(obj)
        case pydantic.BaseModel():
            return obj.dict()

    logger.warning("Type is not JSON serializable: %s", type(obj), extra={"obj": repr(obj)})
    return repr(obj)


class ORJSONResponse(_ORJSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
            default=additionally_serialize,
        )
