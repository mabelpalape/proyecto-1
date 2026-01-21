from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "E-commerce Predictive Analytics"
    DATABASE_URL: str = "sqlite:///./app.db"  # Default to SQLite for MVP
    GEMINI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
