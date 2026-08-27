# Run Config 006A-GPT

_Status: frozen pre-production run configuration_

- Run ID: `006A-GPT`
- Experiment ID: `006-action-representational-compliance`
- Model role: `model_a_gpt`
- Provider/model: `openai/gpt-5.6-sol`
- Samples: 180
- Cells: 6
- Replicates per cell: 30
- Sample namespace: `006A-GPT-`
- Max connections: 1
- Max retries: 3
- Timeout: 60
- Attempt timeout: 45
- Log buffer: 1
- Checkpoint: `turn:1`
- Max output tokens: 4096
- Reasoning effort: `medium`
- Verbosity: `medium`
- Parallel tool calls: disabled
- Temperature/top-p/seed: unsupported or not sent; not relied on
- Manipulation check: same pre-action structured tool schema as all models
- Tool protocol: Inspect tool calls
- Raw logs: ignored under `results/006-action-representational-compliance/run-006A-GPT/`
