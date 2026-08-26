# Provider Comparability Matrix

_Status: pre-production review artifact_

| Dimension | GPT-5.6 Sol reference | 005B Claude Sonnet 5 | 005C Gemini 3.7 Flash |
| --- | --- | --- | --- |
| Provider | OpenAI | Anthropic | Google |
| Inspect model ID | `openai/gpt-5.6-sol` | `anthropic/claude-sonnet-5` | `google/gemini-3.7-flash` |
| Task text | Frozen Experiment 004 | Exact same rendered input | Exact same rendered input |
| Constraint wording | Frozen Experiment 004 | Exact match | Exact match |
| Pressure wording | Frozen Experiment 004 | Exact match | Exact match |
| Manipulation-check schema | Structured tool | Exact same tool schema | Exact same tool schema |
| Tool/action space | Experiment 004 tools | Exact same Inspect tools | Exact same Inspect tools |
| Scoring | Experiment 004 scorer | Exact same scorer | Exact same scorer |
| `--max-tokens 4096` | Exact | Exact flag sent | Exact flag sent |
| `--max-connections 1` | Exact | Exact | Exact |
| `--max-retries 3` | Exact | Exact | Exact |
| `--timeout 60` | Exact | Exact | Exact |
| `--attempt-timeout 45` | Exact | Exact | Exact |
| `--checkpoint turn:1` | Exact | Exact | Exact |
| `--no-parallel-tool-calls` | Exact | Exact flag sent | Exact flag sent |
| Temperature | Not explicitly set | Not explicitly set | Not explicitly set |
| Top-p | Not explicitly set | Not explicitly set | Not explicitly set |
| Seed | No provider-independent seed assumed | Unsupported / not assumed | Unsupported / not assumed |
| Reasoning effort | `medium` sent to GPT-5 | Unsupported / not sent | Unsupported / not sent |
| Verbosity | `medium` sent to GPT-5 | Unsupported / not sent | Unsupported / not sent |
| Structured-output support | Tool call schema | Inspect Anthropic tool calls | Inspect Google tool calls |
| Authentication | OpenAI runner credential | Anthropic runner credential | Google runner credential or ADC |
| Material scientific difference? | Reference | No, if canary/tool preflight passes | No, if canary/tool preflight passes |

The main provider-specific differences are transport and generation-control
surface differences. They are documented before execution and are not changes
to the scientific case, tools, authority, scoring, or outcome definitions.
