from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "E-commerce Backend"
    POSTGRES_URL: str
    MONGO_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    model_config = {
        "env_file": ".env"
    }

settings = Settings()
