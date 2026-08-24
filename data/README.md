# Data Handling

This directory is reserved for experiment observations.

## Intended structure

- `raw/` — immutable raw model trajectories and environment logs
- `processed/` — derived, normalized, or annotated data

## Rules

- Do not edit raw trajectories after collection.
- If a run is invalid, preserve it and flag it with a validity field and reason rather than deleting it.
- Keep model/version, prompt/configuration version, seed, timestamp, and Git commit SHA with each run where available.
- Derived labels, human annotations, and cleaned tables belong under `processed/`, not `raw/`.
- Never commit secrets, credentials, confidential customer data, or prohibited/private datasets.
