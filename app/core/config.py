from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str

    class Config:
        env_file = ".env"

settings = Settings()