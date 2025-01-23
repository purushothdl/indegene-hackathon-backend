from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB_NAME: str
    GCS_BUCKET: str
    GCP_CREDENTIALS_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()