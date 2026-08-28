# Run Configuration: 007C-GEMINI

- Run ID: `007C-GEMINI`
- Model: `google/gemini-3.7-flash`
- Provider: Google/Gemini
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
- Required secret: `GOOGLE_API_KEY` or approved ADC as supported by provider setup
- Raw logs: ignored under `results/007-scenario-suite-pilot/run-007C-GEMINI/inspect/`
