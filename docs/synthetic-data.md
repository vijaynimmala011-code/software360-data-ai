# Synthetic data contract

Module 5 uses only invented organizations, users, commercial terms, events,
and policy content. Generated CSV files are reproducible fixtures and remain
outside Git under `data/generated/`.

## Dataset inventory

| Dataset | Deterministic size | Purpose |
| --- | ---: | --- |
| `organizations.csv` | 10 rows | Fictional business hierarchy |
| `users.csv` | 1,000 rows | Identity and effective-date practice |
| `software_products.csv` | 6 rows | Canonical product dimension |
| `license_contracts.csv` | 6 rows | Fictional cost, seat, and renewal terms |
| `license_assignments.csv` | 2,000 rows | User-to-product entitlements |
| July usage batch | 6,001 rows | 6,000 events plus one exact duplicate |
| August usage batch | 6,000 rows | Later events and a new source column |

## Intentional quality defects

| ID | Stable locator | Intentional defect | Deterministic expectation | Later objective |
| --- | --- | --- | --- | --- |
| DQ-001 | `EVT-000360` | Exact duplicate usage event | The identifier occurs exactly twice | Deduplication and idempotency |
| DQ-002 | `EVT-001360` | Missing `software_id` | Exactly one known null foreign key | Expectations and quarantine |
| DQ-003 | `EVT-002360` | Invalid `session_minutes` | The duration is exactly `-5` | Domain validation |
| DQ-004 | `EVT-003360` | Raw name is `MS TEAMS` | Product 104 remains `Microsoft Teams` | Standardization |
| DQ-005 | `EVT-006360` | July event arrives in August | Event time is July; ingestion time is August | Watermarks and late data |
| DQ-006 | Usage batch headers | Later schema adds `source_system` | July omits it; August includes it | Schema evolution |

## Reproducibility rules

- A fresh `Random(360)` instance is used for every generation.
- Dates, identifiers, column order, filenames, and line endings are fixed.
- Ordered lists are used for random selection; unordered sets are avoided.
- High-volume variable generation belongs in a separate future mode.
