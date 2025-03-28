import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/person_detection")
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost", "http://localhost:80"]
    UPLOAD_DIR: str = "uploads"
    RESULTS_DIR: str = "results"
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    
    class Config:
        env_file = ".env"

def get_settings():
    env = os.getenv("ENV", "development")
    
    if env == "production":
        return ProductionSettings()
    return DevelopmentSettings()

class DevelopmentSettings(Settings):
    DEBUG: bool = True
    
class ProductionSettings(Settings):
    DEBUG: bool = False
    CORS_ORIGINS: list = ["http://localhost", "http://localhost:80"]
    
settings = get_settings() 