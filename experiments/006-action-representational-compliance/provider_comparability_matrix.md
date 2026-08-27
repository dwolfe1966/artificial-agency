# Experiment 006 Provider Comparability Matrix

_Status: pre-results implementation review_

Experiment 006 preserves the same task semantics for all models. Provider
differences below are documented before production execution and should not be
silently normalized after observing outcomes.

| Field | GPT-5.6 Sol | Claude Sonnet 5 | Gemini 3.7 Flash | Classification |
| --- | --- | --- | --- | --- |
| Model ID | `openai/gpt-5.6-sol` | `anthropic/claude-sonnet-5` | `google/gemini-3.7-flash` | experimental factor |
| Provider | OpenAI | Anthropic | Google | experimental factor |
| Tool protocol | Inspect tool calls | Inspect tool calls | Inspect tool calls | transport-only if provider canary passes |
| Structured manipulation check | Same pre-action tool schema | Same pre-action tool schema | Same pre-action tool schema | measurement-equivalent |
| Communication channel | Same `send_customer_message` tool | Same `send_customer_message` tool | Same `send_customer_message` tool | measurement-equivalent |
| Context sufficiency | Expected sufficient | Expected sufficient | Expected sufficient | transport-only if dry-load/canary passes |
| Output-token budget | `4096` | `4096` | `4096` | matched requested budget |
| Temperature/top-p | Not explicitly set | Not explicitly set | Not explicitly set | matched omission |
| Seed | Not sent | Not sent | Not sent | unsupported / not relied on |
| Reasoning controls | `--reasoning-effort medium`, `--verbosity medium` | unsupported / not sent | unsupported / not sent | provider-specific, documented |
| Parallel tool calls | disabled | disabled | disabled | matched requested behavior |
| Retry behavior | Runner/Inspect bounded retries | Runner/Inspect bounded retries | Runner/Inspect bounded retries | transport-only |
| Recovery behavior | Runner v2 missing-ID recovery | Runner v2 missing-ID recovery | Runner v2 missing-ID recovery | transport-only |
| Raw logging | Inspect JSON logs, ignored by Git | Inspect JSON logs, ignored by Git | Inspect JSON logs, ignored by Git | matched |
| Operational status | outcome-blind | outcome-blind | outcome-blind | matched |

## Materiality Review

The model identity factor is scientifically intentional. The only known
provider-specific generation difference is OpenAI-specific reasoning/verbosity
controls; Anthropic and Google runs do not receive approximate substitutes. This
is potentially measurement-affecting and must be reported with results, but it
does not change the semantic task, action space, manipulation check, or scorer.

No scientifically material semantic difference is known at implementation time.
Production launch should remain blocked for any provider that fails model
resolution, tool-call compatibility, structured manipulation-check canary, or
authentication preflight.
