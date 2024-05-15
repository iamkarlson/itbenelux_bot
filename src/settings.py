from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    orevo_sticker: str | None = None
    rand_ratio: int | None = 100


settings = Settings()
