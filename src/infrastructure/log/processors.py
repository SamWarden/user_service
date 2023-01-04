import enum
import inspect
import os
import threading
from collections.abc import Callable, Collection
from typing import Any, ClassVar

import orjson
import structlog
from structlog._utils import get_processname  # noqa
from structlog.processors import CallsiteParameterAdder as _CallsiteParameterAdder

ProcessorType = Callable[
    [
        structlog.types.WrappedLogger, str, structlog.types.EventDict,
    ], str | bytes
]


def additionally_serialize(obj: Any) -> Any:
    raise TypeError(f"TypeError: Type is not JSON serializable: {type(obj)}")


def serialize_to_json(data: Any, default: Any) -> str:
    return orjson.dumps(data, default=additionally_serialize).decode()


class RenderProcessorFactory:
    def __init__(
        self, render_json_logs: bool = False,
        serializer: Callable[..., str | bytes] = serialize_to_json
    ) -> None:
        self._render_json_logs = render_json_logs
        self._serializer = serializer

    def get_processor(self) -> ProcessorType:
        if self._render_json_logs:
            return structlog.processors.JSONRenderer(serializer=self._serializer)
        return structlog.dev.ConsoleRenderer()


class CallsiteParameter(enum.Enum):
    """
    Callsite parameters that can be added to an event dictionary with the
    `structlog.processors.CallsiteParameterAdder` processor class.

    The string values of the members of this enum will be used as the keys for
    the callsite parameters in the event dictionary.

    .. versionadded:: 21.5.0
    """

    #: The full path to the python source file of the callsite.
    PATHNAME = "pathname"
    #: The basename part of the full path to the python source file of the
    #: callsite.
    FILENAME = "filename"
    #: The python module the callsite was in. This mimicks the module attribute
    #: of `logging.LogRecord` objects and will be the basename, without
    #: extension, of the full path to the python source file of the callsite.
    MODULE = "module"
    #: The name of the function that the callsite was in.
    FUNC_NAME = "func_name"
    #: The line number of the callsite.
    LINENO = "lineno"
    #: The ID of the thread the callsite was executed in.
    THREAD = "thread"
    #: The name of the thread the callsite was executed in.
    THREAD_NAME = "thread_name"
    #: The ID of the process the callsite was executed in.
    PROCESS = "process"
    #: The name of the process the callsite was executed in.
    PROCESS_NAME = "process_name"
    #: The relative path to the python source file of the callsite.
    RELPATH = "relpath"


class CallsiteParameterAdder(_CallsiteParameterAdder):
    # Redefine CallsiteParameterAdder class to add RELPATH

    _handlers: ClassVar[
        dict[CallsiteParameter, Callable[[str, inspect.Traceback], Any]]
    ] = {
        CallsiteParameter.PATHNAME: (
            lambda module, frame_info: frame_info.filename
        ),
        CallsiteParameter.FILENAME: (
            lambda module, frame_info: os.path.basename(frame_info.filename)
        ),
        CallsiteParameter.MODULE: (
            lambda module, frame_info: os.path.splitext(
                os.path.basename(frame_info.filename)
            )[0]
        ),
        CallsiteParameter.FUNC_NAME: (
            lambda module, frame_info: frame_info.function
        ),
        CallsiteParameter.LINENO: (
            lambda module, frame_info: frame_info.lineno
        ),
        CallsiteParameter.THREAD: (
            lambda module, frame_info: threading.get_ident()
        ),
        CallsiteParameter.THREAD_NAME: (
            lambda module, frame_info: threading.current_thread().name
        ),
        CallsiteParameter.PROCESS: (lambda module, frame_info: os.getpid()),
        CallsiteParameter.PROCESS_NAME: (
            lambda module, frame_info: get_processname()
        ),
        CallsiteParameter.RELPATH: (
            lambda module, frame_info: os.path.relpath(frame_info.filename)
        ),
    }
    _record_attribute_map: ClassVar[dict[CallsiteParameter, str]] = {
        CallsiteParameter.PATHNAME: "pathname",
        CallsiteParameter.FILENAME: "filename",
        CallsiteParameter.MODULE: "module",
        CallsiteParameter.FUNC_NAME: "funcName",
        CallsiteParameter.LINENO: "lineno",
        CallsiteParameter.THREAD: "thread",
        CallsiteParameter.THREAD_NAME: "threadName",
        CallsiteParameter.PROCESS: "process",
        CallsiteParameter.PROCESS_NAME: "processName",
        CallsiteParameter.RELPATH: "relativePath",
    }
    _all_parameters: ClassVar[set[CallsiteParameter]] = set(CallsiteParameter)

    def __init__(
        self,
        parameters: Collection[CallsiteParameter] = _all_parameters,  # noqa
        additional_ignores: list[str] | None = None,
    ) -> None:
        super().__init__(parameters, additional_ignores)

