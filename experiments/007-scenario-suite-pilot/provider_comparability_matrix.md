# Experiment 007 Provider Comparability Matrix

Status: pre-results implementation artifact.

The scientific task semantics are identical across the three preregistered
models. Provider differences are documented as transport or generation-control
differences and are not used to alter scenario content.

| Field | GPT | Claude | Gemini | Classification |
| --- | --- | --- | --- | --- |
| Frozen model ID | `openai/gpt-5.6-sol` | `anthropic/claude-sonnet-5` | `google/gemini-3.7-flash` | model factor |
| Run ID | `007A-GPT` | `007B-CLAUDE` | `007C-GEMINI` | transport-only |
| Samples | 120 | 120 | 120 | identical |
| Scenarios | refund, procurement, data-access, scheduling | same | same | identical |
| Tool schemas | shared Inspect task tools | shared Inspect task tools | shared Inspect task tools | identical scientific semantics |
| Primary scorer | structured operational state | same | same | identical |
| Natural-language primary scoring | none | none | none | identical |
| Approval/denial mechanics | deterministic denial | same | same | identical |
| Communication channel | `send_update`, non-operational | same | same | identical |
| Retry/recovery | Runner v2 missing-ID recovery | same | same | transport-only |
| Max connections | 1 | 1 | 1 | identical |
| Max retries | 3 | 3 | 3 | identical |
| Timeout | 60 | 60 | 60 | identical |
| Attempt timeout | 45 | 45 | 45 | identical |
| Log buffer | 1 | 1 | 1 | identical |
| Checkpoint | `turn:1` | `turn:1` | `turn:1` | identical |
| OpenAI reasoning controls | `medium` effort and verbosity | unsupported | unsupported | provider-specific generation difference |
| Seed support | not relied on for model randomness | not relied on | not relied on | transport-only |

No scientifically material semantic difference is identified before production
execution. Comparability rests on identical structured environment semantics,
not on pretending provider APIs expose identical generation controls.
