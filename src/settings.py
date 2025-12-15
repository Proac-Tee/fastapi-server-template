from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings loaded from environment variables.
    Automatically loads values from a `.env` file at project root.
    """

    APP_ENV: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str

    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
