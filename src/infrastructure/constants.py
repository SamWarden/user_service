import os

APP_SCOPE = "app"
REQUEST_SCOPE = "request"

CONFIG_PATH: str = os.getenv("CONFIG_PATH", "./config.toml")
