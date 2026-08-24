import hashlib
import sys
from pathlib import Path

import pandas as pd
import pytest

from software360 import cli
from software360.data.generate import generate_all

EXPECTED_GENERATED_FILES = {
    "license_assignments.csv",
    "license_contracts.csv",
    "organizations.csv",
    "software_products.csv",
    "software_usage_events_2025_07.csv",
    "software_usage_events_2025_08.csv",
    "users.csv",
}

EXPECTED_DOCUMENTS = {
    "active_user_policy.md",
    "license_renewal_policy.md",
    "software_security_policy.md",
    "support_runbook.md",
    "utilization_calculation_guide.md",
}


def _file_hashes(directory: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.glob("*.csv"))
    }


def _read_usage_batches(output_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    july = pd.read_csv(output_dir / "software_usage_events_2025_07.csv")
    august = pd.read_csv(output_dir / "software_usage_events_2025_08.csv")
    return july, august


def test_generation_is_reproducible(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    generate_all(first)
    generate_all(second)

    assert {path.name for path in first.glob("*.csv")} == EXPECTED_GENERATED_FILES
    assert _file_hashes(first) == _file_hashes(second)


def test_generated_datasets_have_expected_scale_and_relationships(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "generated"
    generate_all(output_dir)

    organizations = pd.read_csv(output_dir / "organizations.csv")
    users = pd.read_csv(output_dir / "users.csv")
    products = pd.read_csv(output_dir / "software_products.csv")
    contracts = pd.read_csv(output_dir / "license_contracts.csv")
    assignments = pd.read_csv(output_dir / "license_assignments.csv")
    july, august = _read_usage_batches(output_dir)
    events = pd.concat([july, august], ignore_index=True)

    assert len(organizations) == 10
    assert len(users) == 1_000
    assert len(products) == 6
    assert len(contracts) == 6
    assert len(assignments) == 2_000
    assert len(july) == 6_001
    assert len(august) == 6_000
    assert len(events) == 12_001

    organization_ids = set(organizations["organization_id"])
    product_ids = set(products["software_id"])
    user_ids = set(users["user_id"])
    assignment_pairs = set(
        zip(assignments["user_id"], assignments["software_id"], strict=True)
    )

    assert set(users["organization_id"]) <= organization_ids
    assert set(contracts["software_id"]) <= product_ids
    assert set(assignments["user_id"]) <= user_ids
    assert set(assignments["software_id"]) <= product_ids
    assert set(events["user_id"]) <= user_ids
    assert set(events["software_id"].dropna().astype(int)) <= product_ids

    valid_events = events.dropna(subset=["software_id"])
    event_pairs = set(
        zip(
            valid_events["user_id"],
            valid_events["software_id"].astype(int),
            strict=True,
        )
    )
    assert event_pairs <= assignment_pairs


def test_controlled_quality_defects_are_present(tmp_path: Path) -> None:
    output_dir = tmp_path / "generated"
    generate_all(output_dir)

    products = pd.read_csv(output_dir / "software_products.csv")
    july, august = _read_usage_batches(output_dir)
    events = pd.concat([july, august], ignore_index=True)

    duplicate_counts = events["event_id"].value_counts()
    duplicate_ids = set(duplicate_counts[duplicate_counts > 1].index)
    assert duplicate_ids == {"EVT-000360"}
    assert duplicate_counts["EVT-000360"] == 2

    null_software = events.loc[events["software_id"].isna()]
    assert list(null_software["event_id"]) == ["EVT-001360"]

    invalid_duration = events.loc[events["session_minutes"] < 0]
    assert list(invalid_duration["event_id"]) == ["EVT-002360"]
    assert list(invalid_duration["session_minutes"]) == [-5]

    name_variation = events.loc[
        events["source_software_name"] == "MS TEAMS"
    ]
    assert list(name_variation["event_id"]) == ["EVT-003360"]
    assert list(name_variation["software_id"].astype(int)) == [104]
    canonical_name = products.loc[
        products["software_id"] == 104,
        "software_name",
    ].item()
    assert canonical_name == "Microsoft Teams"

    late_event = august.loc[august["event_id"] == "EVT-006360"].iloc[0]
    assert late_event["event_timestamp"].startswith("2025-07-")
    assert late_event["ingested_at"].startswith("2025-08-")

    assert "source_system" not in july.columns
    assert "source_system" in august.columns
    assert set(august["source_system"]) == {"usage-api-v2"}


def test_fictional_documents_are_structured_for_chunking() -> None:
    documents_dir = Path(__file__).resolve().parents[1] / "documents"
    documents = {
        path.name: path.read_text(encoding="utf-8")
        for path in documents_dir.glob("*.md")
    }

    assert set(documents) == EXPECTED_DOCUMENTS
    for content in documents.values():
        normalized_content = " ".join(content.replace(">", " ").split())
        assert content.startswith("# ")
        assert content.count("\n## ") >= 3
        assert "Fictional training document" in content
        assert "contains no confidential information" in normalized_content


def test_cli_generate_data_writes_expected_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["software360", "generate-data"])

    cli.main()

    output_dir = tmp_path / "data" / "generated"
    assert {path.name for path in output_dir.glob("*.csv")} == (
        EXPECTED_GENERATED_FILES
    )
