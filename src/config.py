from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    DATA_BASE_URL: str = ""
    AWS_ACCESS_KEY:str=""
    AWS_SECRET_KEY:str=""
    S3_BUCKET_NAME:str=""
    REGION_NAME:str=""


    SECRET_KEY: str=""
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 60 #defect
    ALGORITHM:str = ""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent/ ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()