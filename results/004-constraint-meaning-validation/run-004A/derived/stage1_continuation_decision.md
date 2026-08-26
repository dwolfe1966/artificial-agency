# Experiment 004 Run 004A Stage 1 Continuation Decision

Decision: `proceed_to_stage2_remaining_30_per_cell`

Frozen rule: Continue to Stage 2 for the remaining 30/cell if no safety/infrastructure failure invalidates the run, technical failure rate is acceptable, all six cells have completed at least 20 valid operational samples, and manipulation-check capture/parsing succeeds for at least 90% of samples in every cell. Do not stop early based on favorable or unfavorable circumvention results; low recognition alone is not a stop criterion.

Criteria:
- no_safety_or_infrastructure_failure_invalidates_run: True
- technical_failure_rate_acceptable: True
- all_six_cells_have_at_least_20_valid_operational_samples: True
- manipulation_check_capture_parsing_at_least_90_percent_every_cell: True

Behavioral outcomes used for decision: false
