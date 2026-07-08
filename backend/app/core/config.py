from functools import lru_cache
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env.secrets",
		env_file_encoding="utf-8",
		case_sensitive=True,
		extra="ignore",
	)

	APP_NAME: str = "ResearchMind AI"
	APP_DESCRIPTION: str = "AI research assistant built with FastAPI and RAG"
	APP_VERSION: str = "0.1.0"
	API_V1_PREFIX: str = "/api/v1"

	POSTGRES_HOST: str = "postgres"
	POSTGRES_PORT: int = 5432
	POSTGRES_USER: str = "researchmind"
	POSTGRES_PASSWORD: str = "researchmind"
	POSTGRES_DB: str = "researchmind"
	DATABASE_URL: str | None = None
	DOCUMENT_STORAGE_PATH: str = "/app/storage"
	MAX_UPLOAD_SIZE_MB: int = 50
	CHUNK_SIZE: int = 1000
	CHUNK_OVERLAP: int = 200
	EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"
	EMBEDDING_DIMENSION: int = 384
	EMBEDDING_BATCH_SIZE: int = 32
	GEMINI_API_KEY: str | None = None
	GEMINI_MODEL_NAME: str = "gemini-2.5-flash"
	CHAT_TOP_K: int = 5
	CHAT_MIN_SIMILARITY: float = 0.2

	BACKEND_CORS_ORIGINS: Annotated[list[str], NoDecode] = Field(
		default_factory=lambda: ["http://localhost:3000"]
	)

	@field_validator("BACKEND_CORS_ORIGINS", mode="before")
	@classmethod
	def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
		if isinstance(value, str):
			return [origin.strip() for origin in value.split(",") if origin.strip()]
		return value

	@property
	def sqlalchemy_database_url(self) -> str:
		if self.DATABASE_URL:
			return self.DATABASE_URL

		return (
			"postgresql+psycopg://"
			f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
			f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
		)


@lru_cache()
def get_settings() -> Settings:
	return Settings()


settings = get_settings()
