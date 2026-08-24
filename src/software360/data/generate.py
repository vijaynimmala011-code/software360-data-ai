from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from random import Random

import pandas as pd

OUT = Path("data/generated")
SEED = 360
USER_COUNT = 1_000
EVENTS_PER_BATCH = 6_000

PRODUCT_RECORDS = (
    {
        "software_id": 101,
        "software_name": "Tableau",
        "vendor": "Example BI",
        "category": "Analytics",
        "license_type": "named_user",
    },
    {
        "software_id": 102,
        "software_name": "Power BI",
        "vendor": "Example Cloud",
        "category": "Analytics",
        "license_type": "capacity",
    },
    {
        "software_id": 103,
        "software_name": "Slack",
        "vendor": "Example Collaboration",
        "category": "Collaboration",
        "license_type": "seat",
    },
    {
        "software_id": 104,
        "software_name": "Microsoft Teams",
        "vendor": "Example Productivity",
        "category": "Collaboration",
        "license_type": "seat",
    },
    {
        "software_id": 105,
        "software_name": "GitHub Enterprise",
        "vendor": "Example Development",
        "category": "Engineering",
        "license_type": "named_user",
    },
    {
        "software_id": 106,
        "software_name": "ServiceNow",
        "vendor": "Example Workflow",
        "category": "Operations",
        "license_type": "named_user",
    },
)

EVENT_TYPES = ("login", "view", "edit", "export", "message", "meeting")
EVENT_WEIGHTS = (10, 25, 20, 5, 25, 15)


def _build_products() -> pd.DataFrame:
    return pd.DataFrame.from_records(PRODUCT_RECORDS)


def _build_organizations(rng: Random) -> pd.DataFrame:
    records = [
        {
            "organization_id": organization_id,
            "organization_name": f"Org {organization_id}",
            "region": rng.choice(("Central", "East", "West")),
        }
        for organization_id in range(1, 11)
    ]
    return pd.DataFrame.from_records(records)


def _build_users(rng: Random) -> pd.DataFrame:
    departments = ("Engineering", "Finance", "Operations")
    start_anchor = date(2023, 1, 1)
    records = []
    for user_id in range(1, USER_COUNT + 1):
        effective_from = start_anchor + timedelta(days=rng.randint(0, 729))
        effective_to = "2025-12-31" if rng.random() < 0.08 else ""
        records.append(
            {
                "user_id": user_id,
                "organization_id": rng.randint(1, 10),
                "user_name": f"User {user_id:04d}",
                "department": rng.choice(departments),
                "effective_from": effective_from.isoformat(),
                "effective_to": effective_to,
            }
        )
    return pd.DataFrame.from_records(records)


def _build_contracts() -> pd.DataFrame:
    commercial_terms = (
        (101, 125_000, 600),
        (102, 96_000, 800),
        (103, 84_000, 1_000),
        (104, 110_000, 1_000),
        (105, 132_000, 500),
        (106, 150_000, 400),
    )
    records = [
        {
            "contract_id": f"CON-{software_id}",
            "software_id": software_id,
            "annual_cost": annual_cost,
            "seats": seats,
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
        }
        for software_id, annual_cost, seats in commercial_terms
    ]
    return pd.DataFrame.from_records(records)


def _build_assignments(
    rng: Random,
) -> tuple[pd.DataFrame, list[tuple[int, int]]]:
    software_ids = [record["software_id"] for record in PRODUCT_RECORDS]
    records = []
    assignment_pairs = []
    assignment_id = 1
    assignment_anchor = date(2025, 1, 1)
    revocation_anchor = date(2025, 9, 1)

    for user_id in range(1, USER_COUNT + 1):
        for software_id in rng.sample(software_ids, k=2):
            assigned_at = assignment_anchor + timedelta(days=rng.randint(0, 150))
            revoked_at = ""
            if rng.random() < 0.08:
                revoked_at = (
                    revocation_anchor + timedelta(days=rng.randint(0, 90))
                ).isoformat()
            records.append(
                {
                    "assignment_id": f"ASN-{assignment_id:06d}",
                    "user_id": user_id,
                    "software_id": software_id,
                    "assigned_at": assigned_at.isoformat(),
                    "revoked_at": revoked_at,
                }
            )
            assignment_pairs.append((user_id, software_id))
            assignment_id += 1

    return pd.DataFrame.from_records(records), assignment_pairs


def _format_timestamp(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_usage_batches(
    rng: Random,
    assignment_pairs: list[tuple[int, int]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    product_names = {
        record["software_id"]: record["software_name"]
        for record in PRODUCT_RECORDS
    }
    batch_starts = (
        datetime(2025, 7, 1, tzinfo=UTC),
        datetime(2025, 8, 1, tzinfo=UTC),
    )
    max_minute_offset = (28 * 24 * 60) - 1
    records = []

    for event_number in range(1, (EVENTS_PER_BATCH * 2) + 1):
        batch_index = 0 if event_number <= EVENTS_PER_BATCH else 1
        event_at = batch_starts[batch_index] + timedelta(
            minutes=rng.randint(0, max_minute_offset)
        )
        ingested_at = event_at + timedelta(hours=rng.randint(0, 36))
        user_id, software_id = rng.choice(assignment_pairs)
        records.append(
            {
                "event_id": f"EVT-{event_number:06d}",
                "user_id": user_id,
                "software_id": software_id,
                "source_software_name": product_names[software_id],
                "event_timestamp": _format_timestamp(event_at),
                "event_type": rng.choices(
                    EVENT_TYPES,
                    weights=EVENT_WEIGHTS,
                    k=1,
                )[0],
                "session_minutes": rng.randint(1, 180),
                "ingested_at": _format_timestamp(ingested_at),
            }
        )

    records[359]["event_id"] = "EVT-000360"
    records[1_359]["event_id"] = "EVT-001360"
    records[1_359]["software_id"] = None
    records[2_359]["event_id"] = "EVT-002360"
    records[2_359]["session_minutes"] = -5

    teams_user_id, _ = next(
        pair for pair in assignment_pairs if pair[1] == 104
    )
    records[3_359].update(
        {
            "event_id": "EVT-003360",
            "user_id": teams_user_id,
            "software_id": 104,
            "source_software_name": "MS TEAMS",
        }
    )
    records[6_359].update(
        {
            "event_id": "EVT-006360",
            "event_timestamp": "2025-07-31T23:45:00Z",
            "ingested_at": "2025-08-05T08:00:00Z",
        }
    )

    columns = [
        "event_id",
        "user_id",
        "software_id",
        "source_software_name",
        "event_timestamp",
        "event_type",
        "session_minutes",
        "ingested_at",
    ]
    events = pd.DataFrame.from_records(records, columns=columns)
    events["software_id"] = events["software_id"].astype("Int64")

    july = events.iloc[:EVENTS_PER_BATCH].copy()
    duplicate = july.loc[july["event_id"] == "EVT-000360"].copy()
    july = pd.concat([july, duplicate], ignore_index=True)

    august = events.iloc[EVENTS_PER_BATCH:].copy()
    august["source_system"] = "usage-api-v2"
    return july, august


def _write_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(
        path,
        index=False,
        encoding="utf-8",
        lineterminator="\n",
        na_rep="",
    )


def generate_all(output_dir: Path = OUT, seed: int = SEED) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = Random(seed)

    products = _build_products()
    organizations = _build_organizations(rng)
    users = _build_users(rng)
    contracts = _build_contracts()
    assignments, assignment_pairs = _build_assignments(rng)
    july_events, august_events = _build_usage_batches(rng, assignment_pairs)

    datasets = {
        "software_products.csv": products,
        "organizations.csv": organizations,
        "users.csv": users,
        "license_contracts.csv": contracts,
        "license_assignments.csv": assignments,
        "software_usage_events_2025_07.csv": july_events,
        "software_usage_events_2025_08.csv": august_events,
    }
    for filename, frame in datasets.items():
        _write_csv(frame, output_dir / filename)


if __name__ == "__main__":
    generate_all()
