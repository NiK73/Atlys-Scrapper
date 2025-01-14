from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TOKEN: str = "123"
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
