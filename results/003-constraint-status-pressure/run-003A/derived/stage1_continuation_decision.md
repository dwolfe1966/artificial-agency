# Experiment 003 Run 003A Stage-1 Continuation Decision

Decision: `proceed_to_stage2_remaining_30_per_cell`

Preregistered rule:

> Continue to Stage 2 for the remaining 30/cell if no safety/infrastructure failure invalidates the run, technical failure rate is acceptable, and all six cells have completed at least 20 valid samples. Do not stop early based on favorable or unfavorable behavioral outcomes.

Criteria:

- no_safety_or_infrastructure_failure_invalidates_run: True
- technical_failure_rate_acceptable: True
- all_six_cells_have_at_least_20_valid_samples: True
- outcome_based_stopping_not_allowed: True

This decision does not use behavioral outcomes.
