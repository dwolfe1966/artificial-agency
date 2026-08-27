# Run Config 006B-CLAUDE

_Status: frozen pre-production run configuration_

- Run ID: `006B-CLAUDE`
- Experiment ID: `006-action-representational-compliance`
- Model role: `model_b_claude`
- Provider/model: `anthropic/claude-sonnet-5`
- Samples: 180
- Cells: 6
- Replicates per cell: 30
- Sample namespace: `006B-CLAUDE-`
- Max connections: 1
- Max retries: 3
- Timeout: 60
- Attempt timeout: 45
- Log buffer: 1
- Checkpoint: `turn:1`
- Max output tokens: 4096
- Reasoning effort: unsupported / not sent
- Verbosity: unsupported / not sent
- Parallel tool calls: disabled
- Temperature/top-p/seed: unsupported or not sent; not relied on
- Manipulation check: same pre-action structured tool schema as all models
- Tool protocol: Inspect tool calls
- Raw logs: ignored under `results/006-action-representational-compliance/run-006B-CLAUDE/`
