# Experiment 005 Cross-Model Comparability

| Model | Provider | Tool protocol | Structured check | Generation differences | Classification |
| --- | --- | --- | --- | --- | --- |
| GPT-5.6 Sol | OpenAI | Inspect OpenAI tool calls | Experiment 004 structured tool | GPT reasoning/verbosity flags sent in reference run | reference |
| Claude Sonnet 5 | Anthropic | Inspect Anthropic tool calls | Same schema and timing | GPT reasoning/verbosity unsupported; no seed equivalence assumed | transport-only / generation-control surface difference |
| Gemini 3.7 Flash | Google | Inspect Google tool calls | Same schema and timing | GPT reasoning/verbosity unsupported; no seed equivalence assumed | transport-only / generation-control surface difference |

No scientific prompt, authority rule, action space, scorer, or outcome-definition changes were made for the comparison models.

Manipulation-check success rates are reported in the quantitative summaries and are not used to exclude models from ITT analysis.
