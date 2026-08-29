# Experiment 008 Provider Comparability Matrix

_Status: pre-results implementation artifact._

## Models

| Run | Provider | Model ID | Samples | Notes |
| --- | --- | --- | ---: | --- |
| `008A-GPT` | OpenAI | `openai/gpt-5.6-sol` | 120 | OpenAI reasoning controls documented where supported. |
| `008B-CLAUDE` | Anthropic | `anthropic/claude-sonnet-5` | 120 | No OpenAI-specific reasoning flags. |
| `008C-GEMINI` | Google | `google/gemini-3.7-flash` | 120 | No OpenAI-specific reasoning flags. |

## Tool Semantics

All models receive the same Inspect tool schemas:

- workflow/case inspection tools;
- approval request tool;
- procurement operational tools;
- data-access operational tools;
- communication update tool;
- post-action evaluation-awareness tool.

Provider differences are expected to be transport/configuration differences,
not scientific semantics.

## Generation Controls

| Setting | GPT | Claude | Gemini | Classification |
| --- | --- | --- | --- | --- |
| model ID | exact | exact | exact | transport/config |
| max output tokens | `4096` | `4096` | `4096` | matched where supported |
| max connections | `1` | `1` | `1` | exact |
| retries | `3` | `3` | `3` | exact runner setting |
| timeout | `60` | `60` | `60` | exact runner setting |
| attempt timeout | `45` | `45` | `45` | exact runner setting |
| checkpoint | `turn:1` | `turn:1` | `turn:1` | exact runner setting |
| reasoning effort | `medium` | unsupported | unsupported | provider-specific transport/config |
| verbosity | `medium` | unsupported | unsupported | provider-specific transport/config |
| seed | not relied on | not relied on | not relied on | unsupported/mixed |

## Structured Awareness Compatibility

The awareness measure is a structured tool call with categorical string fields.
It does not require provider-native JSON schema output beyond normal Inspect
tool/function calling.

## Comparability Classification

Pre-results classification: PASS.

No known provider difference materially changes the formal authority boundary,
available operational actions, deterministic denial, primary scoring, or
post-action awareness schema. Unsupported reasoning/verbosity/seed controls are
documented rather than silently normalized.
