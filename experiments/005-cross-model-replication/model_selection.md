# Experiment 005 Model Selection

_Status: preregistered model-selection rationale_

## Selection Principle
Models are selected for capability comparability, provider diversity,
post-training diversity, technical feasibility, and reproducibility. They are
not selected because they are expected to violate constraints.

The exact model IDs below were checked against current primary provider and
Inspect documentation on 2026-08-26. Availability, account access, quota, and
provider package installation must be rechecked immediately before execution.

## Reference Model A
`openai/gpt-5.6-sol`

Rationale:

- already used in Experiment 004;
- provides the baseline constraint-bounded reference result;
- completed the structured manipulation-check/tool protocol with 0 technical
  failures across 300 samples.

Reference result:

- Experiment 004 final quantitative results:
  `1ab0fcb335ade07f212b7162ee657689c8ee7c04`.

## First Comparison Model B
`anthropic/claude-sonnet-5`

Rationale:

- different provider/lab from OpenAI;
- current Claude documentation identifies Claude Sonnet 5 as a current model
  balancing speed and intelligence;
- current Anthropic model docs identify tool use support for current models;
- Inspect provides a first-party `anthropic/` model provider interface;
- expected to be technically capable of multi-step tool-use evaluation without
  changing the Experiment 004 task content.

Pre-execution requirements:

- Anthropic API credential available only in the runner environment;
- Anthropic provider SDK installed if not already present;
- no credential printing;
- no provider-specific prompt edits;
- dry-load and nonexperimental canary pass before production samples.

## Next Planned Comparison Model C
`google/gemini-3.7-flash`

Rationale:

- different provider/lab from OpenAI and Anthropic;
- current Gemini API documentation lists `gemini-3.7-flash` as a stable Gemini
  model intended for complex coding, agentic workflows, and multi-step
  execution;
- Inspect provides a `google/` provider interface;
- stable endpoint is preferred over preview endpoints for reproducibility.

Pre-execution requirements:

- Google API credential or approved Google ADC setup available only in the
  runner environment;
- `google-genai` provider SDK installed if not already present;
- no credential printing;
- no provider-specific prompt edits;
- dry-load and nonexperimental canary pass before production samples.

## Deferred / Backup Candidates
Backup candidates may be recorded later only before results from the relevant
comparison model are inspected. Any substitution must be justified by provider
availability, quota, tool support, or cost/access constraints, not by observed
behavior.

Possible backup categories:

- another current Anthropic model if Sonnet 5 access is unavailable;
- another stable Gemini text/tool model if Gemini 3.7 Flash access is
  unavailable;
- a strong open-weight hosted model only if tool protocol compatibility and
  reproducibility are established before execution.

## Documentation Sources
Current model availability and provider feasibility were checked against:

- Anthropic Claude model overview and model-ID/versioning documentation;
- Google Gemini API model documentation;
- Inspect model-provider documentation for Anthropic and Google support.

Source URLs checked on 2026-08-26:

- `https://platform.claude.com/docs/en/models/overview`
- `https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions`
- `https://ai.google.dev/gemini-api/docs/models`
- `https://inspect.aisi.org.uk/providers.html`

Record exact source URLs and access date in the run metadata before execution.
