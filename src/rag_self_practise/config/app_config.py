from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Settings read from config.toml for a single ingestion run."""

    collection_name: str
    json_path: str
