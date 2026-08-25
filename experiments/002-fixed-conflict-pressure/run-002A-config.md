# Experiment 002 Run 002A Configuration

_Status: prepared; do not execute without explicit approval_

## Inspect Task
`artificial_agency/experiments/exp002/inspect_task.py@exp002_fixed_conflict_phase1`

Packaged task name:
`exp002_fixed_conflict_phase1`

## Initial Model
`openai/gpt-5.6-sol`

## Command
```bash
.venv/bin/inspect eval \
  artificial_agency/experiments/exp002/inspect_task.py@exp002_fixed_conflict_phase1 \
  --model openai/gpt-5.6-sol \
  --max-tokens 4096 \
  --reasoning-effort medium \
  --verbosity medium \
  --no-parallel-tool-calls \
  --epochs 1 \
  --max-connections 1 \
  --log-format json \
  --log-dir results/002-fixed-conflict-pressure/run-002A/inspect \
  --tags exp002,phase1,run002A,fixed-conflict-pressure \
  --metadata experiment_id=002-fixed-conflict-pressure \
  --metadata phase=fixed_conflict_pressure \
  --metadata run_id=run-002A
```

Add `--metadata git_commit=<implementation-sha>` immediately before launch.

## Raw-Log Policy
Raw Inspect logs remain outside Git. Derived results, manifests/checksums, experiment definitions, predictions, and analysis artifacts are tracked.
