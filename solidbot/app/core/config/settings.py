import os
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = PostgresDsn.build(
        scheme="postgresql",
        username="user",
        password="password",
        host="localhost",
        port=5432,
        path="/sii_rag",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()