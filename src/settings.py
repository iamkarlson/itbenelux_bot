from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    orevo_sticker: str
    rand_ratio: int


settings = Settings()
