from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiV1(BaseModel):
    """Настройки маршрутов API версии 1"""
    auth: str = "/auth"
    reservations: str = "/reservations"
    users: str = "/users"
    rooms: str = "/rooms"


class ApiSettings(BaseModel):
    """Общие настройки API"""
    prefix: str = "/api"
    v1: ApiV1 = ApiV1()


class AccessToken(BaseModel):
    """Настройки JWT токена"""
    algorithm: str = "HS256"
    type: str = "Bearer"
    expire_time: int = 10  # minutes
    secret_key: str


class DatabaseSettings(BaseModel):
    """Настройки подключения к PostgreSQL"""
    username: str
    password: str
    host: str
    port: int
    name: str
    echo: bool

    @property
    def url(self) -> str:
        """Формирует URL для подключения к БД"""
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    """Главный класс настроек"""
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    host: str
    port: int
    db: DatabaseSettings
    token: AccessToken
    api: ApiSettings = ApiSettings()


settings = Settings()
