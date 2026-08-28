# Run Configuration: 007B-CLAUDE

- Run ID: `007B-CLAUDE`
- Model: `anthropic/claude-sonnet-5`
- Provider: Anthropic
- Samples: 120
- Scenarios: 30 each for refund, procurement, data-access, scheduling
- Max connections: 1
- Max retries: 3
- Timeout: 60
- Attempt timeout: 45
- Log buffer: 1
- Checkpoint: `turn:1`
- Max output tokens: 4096
- OpenAI-specific reasoning/verbosity controls: unsupported and not approximated
- Parallel tool calls: disabled
- Required secret: `ANTHROPIC_API_KEY`
- Raw logs: ignored under `results/007-scenario-suite-pilot/run-007B-CLAUDE/inspect/`
