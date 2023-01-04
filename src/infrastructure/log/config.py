from dataclasses import dataclass
from pathlib import Path


@dataclass
class LoggingConfig:
    render_json_logs: bool = False
    path: Path | None = None
    level: str = "DEBUG"
