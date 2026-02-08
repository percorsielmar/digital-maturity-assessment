from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    DATABASE_URL: str = "postgresql+asyncpg://neondb_owner:npg_gPSLt8r3VxQd@ep-steep-mouse-agbjbjq7-pooler.c-2.eu-central-1.aws.neon.tech/neondb?ssl=require"
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
