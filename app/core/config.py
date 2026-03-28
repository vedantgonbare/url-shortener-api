from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis (already in your .env)
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        extra = "ignore"  #  ignore any extra .env variables we haven't defined yet

settings = Settings()