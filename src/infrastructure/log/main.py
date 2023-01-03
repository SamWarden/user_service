import logging.config
import os
from typing import Any

import structlog
from sqlalchemy import log as sa_log

from .config import LoggingConfig
from .processors import CallsiteParameter, CallsiteParameterAdder, RenderProcessorFactory


def configure_logging(cfg: LoggingConfig) -> dict[str, Any]:
    # Mute SQLAlchemy default logger handler
    sa_log._add_default_handler = lambda _: None  # type: ignore

    render_processor = RenderProcessorFactory(cfg.render_json_logs).get_processor()
    time_stamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True)
    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),
        time_stamper,
    ]
    if cfg.path:
        cfg.path.parent.mkdir(parents=True, exist_ok=True)
        log_path = cfg.path / "logs.log" if cfg.path.is_dir() else cfg.path
    else:
        log_path = None

    print(log_path)
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    # TODO: add processor that will add extra fields to a record
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    render_processor,
                ],
                "foreign_pre_chain": pre_chain,
            },
            "default": {
                "format": '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                "datefmt": '%Y-%m-%d %H:%M:%S',
            },
        },
        "handlers": {
            "default": {
                "level": cfg.level,
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
            "file": {
                "level": cfg.level,
                "class": "logging.FileHandler",
                "filename": log_path if log_path else os.devnull,
                "formatter": "default",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "file"],
                "level": cfg.level,
                "propagate": True,
            },
            "gunicorn.access": {"handlers": ["default"]},
            "gunicorn.error": {"handlers": ["default"]},
            "uvicorn.access": {"handlers": ["default"]},
        },
        "root": {
            "level": cfg.level,
            "handlers": ["default", 'file'],
        },
    }

    logging.config.dictConfig(config)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            CallsiteParameterAdder((
                CallsiteParameter.RELPATH,
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            )),
            structlog.stdlib.PositionalArgumentsFormatter(),
            time_stamper,
            structlog.processors.StackInfoRenderer(),
            # structlog.processors.format_exc_info,  # print exceptions from event dict
            # structlog.processors.UnicodeDecoder(),  # convert bytes to str
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            # structlog.stdlib.render_to_log_kwargs,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        # wrapper_class=structlog.stdlib.AsyncBoundLoggerd,  # type: ignore  # noqa
        wrapper_class=structlog.stdlib.BoundLogger,  # type: ignore  # noqa
        cache_logger_on_first_use=True,
    )
    return config
