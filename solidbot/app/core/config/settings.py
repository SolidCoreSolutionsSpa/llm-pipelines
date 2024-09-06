import os
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
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

    @property
    def DATABASE_URL_STR(self) -> str:
        return self.DATABASE_URL.unicode_string()

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

settings = Settings()