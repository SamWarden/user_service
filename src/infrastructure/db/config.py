from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "test"
    user: str = ""
    password: str = ""
    echo: bool = True

    @property
    def full_url(self) -> str:
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.database,
        )
