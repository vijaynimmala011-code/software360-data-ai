from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: Literal["dev", "test", "prod"] = "dev"
    catalog_prefix: str = "software360"
    schema_bronze: str = "bronze"
    schema_silver: str = "silver"
    schema_gold: str = "gold"
    schema_ai: str = "ai"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="S360_",
        extra="ignore",
    )

    @property
    def catalog(self) -> str:
        return f"{self.catalog_prefix}_{self.environment}"

    def table_name(self, schema: str, table: str) -> str:
        allowed = {
            self.schema_bronze,
            self.schema_silver,
            self.schema_gold,
            self.schema_ai,
        }
        if schema not in allowed:
            raise ValueError(f"Unsupported schema: {schema}")
        return f"{self.catalog}.{schema}.{table}"


def load_settings() -> Settings:
    return Settings()
