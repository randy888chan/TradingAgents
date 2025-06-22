import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trading Platform API"
    API_V1_STR: str = "/api/v1"

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_in_env_file")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tradingdb")

    class Config:
        case_sensitive = True
        # env_file = ".env" # Handled by load_dotenv() for more flexibility

settings = Settings()
