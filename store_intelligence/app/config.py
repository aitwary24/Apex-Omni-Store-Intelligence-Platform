# app/config.py
import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Apex Omni-Store Intelligence Platform"
    APP_VERSION: str = "12.0.0"
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    
    # Database configuration string fallback
    DATABASE_URL: str = Field(
        default="postgresql://postgres:admin%40ankit@localhost:5432/store_intelligence",
        env="DATABASE_URL"
    )
    
    POS_DATA_FILE: str = Field(default="Brigade_Bangalore_10_April_26 (1)bc6219c (1).csv", env="POS_DATA_FILE")
    LAYOUT_DATA_FILE: str = Field(default="Brigade Road - Store layoutc5f5d56 (1).xlsx - Sheet1.csv", env="LAYOUT_DATA_FILE")
    VIDEO_ASSET_DIR: str = Field(default=".", env="VIDEO_ASSET_DIR")

    class Config:
        # Resolves env file relative to the execution root folder cleanly
        env_file = os.path.join(os.getcwd(), ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()