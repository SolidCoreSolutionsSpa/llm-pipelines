import os
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, HttpUrl
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = PostgresDsn.build(
        scheme="postgresql",
        username="user",
        password="password",
        host="localhost",
        port=5432,
        path="/sii_rag",
    )
    OPENAI_API_KEY: str
    EMBEDDING_API_URL: HttpUrl = os.getenv("EMBEDDING_API_URL")
    EMBEDDING_MODEL: str =os.getenv("EMBEDDING_MODEL")

    @property
    def DATABASE_URL_STR(self) -> str:
        return self.DATABASE_URL.unicode_string()

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()