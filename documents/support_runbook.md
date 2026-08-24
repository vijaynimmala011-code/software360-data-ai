# Software 360 Support Runbook

> **Fictional training document.** All organizations, people, rules,
> thresholds, dates, costs, contacts, and examples are invented for Software
> 360. This is not an operational company runbook and contains no confidential
> information.

## 1. Purpose and supported workflows

This runbook covers fictional configuration, synthetic generation, ingestion,
quality, transformation, retrieval, agent, and API support scenarios.

## 2. Initial triage

Capture the command, timestamp, environment name, sanitized error, and affected
artifact. Do not record tokens, passwords, connection strings, or raw `.env`
content.

## 3. Data-generation failures

Rerun the deterministic generator with seed 360. Confirm the expected files,
row counts, and hashes before changing generator logic.

## 4. Data-quality alerts

Compare the alert with the committed defect catalog. Documented synthetic
defects are expected fixtures; any additional defect requires investigation.

## 5. Metric discrepancies

Check assignment eligibility, qualifying event types, duplicate identifiers,
late records, and reporting grain before recalculating a metric.

## 6. Recovery and validation

Restore the last verified input, rerun the affected deterministic step, then
run pytest, Ruff, and the hash comparison. Preserve the failure evidence.

## 7. Escalation and closeout

Escalate to fictional role owners based on the affected boundary. Close the
case only after validation passes and the resolution is documented without
secret values.
