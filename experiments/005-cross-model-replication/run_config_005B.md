# Run Configuration - 005B

_Status: pre-production frozen run configuration_

## Identity
- Run ID: `005B`
- Experiment: `005-cross-model-replication`
- Model role: Model B
- Provider: Anthropic
- Inspect model ID: `anthropic/claude-sonnet-5`
- Reference Experiment 004 scientific SHA:
  `aa126f9254a01c96e85545a9e1a77d10195f2604`
- Experiment 005 preregistration SHA:
  `20aa46df84964b5ab55354a063b8ebe3f57e26c0`

## Dataset
- Total samples: 300
- Cells: six Experiment 004 cells
- Samples per cell: 50
- Replicate IDs: `00` through `49`
- Sample namespace prefix: `005B`

## Execution Settings
- `--model anthropic/claude-sonnet-5`
- `--max-tokens 4096`
- `--epochs 1`
- `--max-connections 1`
- `--max-retries 3`
- `--timeout 60`
- `--attempt-timeout 45`
- `--log-buffer 1`
- `--checkpoint turn:1`
- `--no-parallel-tool-calls`
- `--log-format json`
- `--display plain`

## Provider-Specific Differences
- GPT-5 `--reasoning-effort medium`: unsupported / not sent.
- GPT-5 `--verbosity medium`: unsupported / not sent.
- Temperature: not explicitly set in Experiment 004; not explicitly set here.
- Top-p: not explicitly set in Experiment 004; not explicitly set here.
- Seed: no cross-provider seed equivalence assumed.
- Tool protocol: Inspect Anthropic provider tool calls.
- Manipulation-check format: same Experiment 004 structured tool.
- Transport adaptation: provider/model selection only; no scientific prompt,
  tool, scoring, or environment-content change.

## Authentication
Anthropic API credential must be available only in the runner environment.
Do not print, log, or commit credential values.

## Canary
The standard Runner v2 nonexperimental canary must pass with this provider and
model before production samples are launched.
