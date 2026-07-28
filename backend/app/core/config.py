from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Crypto Agility Scanner"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = (
        "postgresql://postgres:postgres@postgres:5432/crypto_scanner"
    )

    REDIS_URL: str = "redis://redis:6379"

    SECRET_KEY: str = "change_this_in_production"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()