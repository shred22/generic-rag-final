import tomllib
from pathlib import Path

from rag_self_practise.config.app_config import AppConfig


class TomlConfigLoader:
    """Reads ingestion settings from a config.toml file."""

    def load(self, config_path: str) -> AppConfig:
        with Path(config_path).open("rb") as config_file:
            data = tomllib.load(config_file)

        if "ingestion" not in data:
            raise ValueError(f"Missing [ingestion] section in {config_path}")

        ingestion = data["ingestion"]
        for key in ("collection_name", "json_path"):
            if key not in ingestion:
                raise ValueError(f"Missing '{key}' in [ingestion] section of {config_path}")

        return AppConfig(
            collection_name=ingestion["collection_name"],
            json_path=ingestion["json_path"],
        )
