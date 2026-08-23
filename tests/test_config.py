from pathlib import Path

import pytest

from software360.common.config import Settings, load_settings


def test_valid_table_name() -> None:
    settings = Settings(environment="dev")

    assert (
        settings.table_name("bronze", "usage_events_raw")
        == "software360_dev.bronze.usage_events_raw"
    )


def test_invalid_schema_is_rejected() -> None:
    settings = Settings()

    with pytest.raises(ValueError, match=r"^Unsupported schema: secret$"):
        settings.table_name("secret", "customer_data")


def test_environment_variable_changes_catalog(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("S360_ENVIRONMENT", "prod")
    monkeypatch.setenv("S360_CATALOG_PREFIX", "software360")

    settings = load_settings()

    assert settings.environment == "prod"
    assert settings.catalog == "software360_prod"
