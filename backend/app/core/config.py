from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

    
class Settings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  
        
    PROJECT_NAME: str = "Sentinel Nexus"
    API_V1_STR: str = "/api/v1"
    
    # CORS configuration
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost",
        "http://localhost:3000",  # Default Nuxt dev server
        "http://localhost:8000",  # FastAPI Swagger UI
    ]

    # @field_validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "ckiprotich"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "nexus"
    # Remove SQLALCHEMY_DATABASE_URI and validator; use a property instead

    @property
    def db_url(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_SERVER
        db = self.POSTGRES_DB
        return f"postgresql+asyncpg://{user}:{password}@{host}/{db}"

    @property
    def sync_db_url(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_SERVER
        db = self.POSTGRES_DB
        return f"postgresql+psycopg2://{user}:{password}@{host}/{db}"

    # JWT configuration
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Bright Data API configuration
    BRIGHT_DATA_API_KEY: Optional[str] = None
    BRIGHT_DATA_USERNAME: Optional[str] = None
    BRIGHT_DATA_PASSWORD: Optional[str] = None
    WEB_UNLOCKER_ZONE: Optional[str] = None
    BROWSER_AUTH: Optional[str] = None
    
    
    # LLM configuration
    OPENROUTER_API_KEY: Optional[str] = None
    DEFAULT_LLM_MODEL: str = "openrouter/google/gemini-2.0-flash-exp:free"

    SOURCE_COMMIT: Optional[str] = None
    COOLIFY_URL: Optional[str] = None
    COOLIFY_FQDN: Optional[str] = None
    COOLIFY_BRANCH: Optional[str] = None
    COOLIFY_RESOURCE_UUID: Optional[str] = None
    COOLIFY_CONTAINER_NAME: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    PORT: Optional[str] = "8001"
    HOST: Optional[str] = "0.0.0.0"


settings = Settings()
