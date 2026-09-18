from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ChronoMed"
    debug: bool = True
    database_url: str = ""


settings = Settings()