# Structured Output Compatibility Review

_Status: pre-production review artifact_

The Experiment 004 manipulation-check content is reused unchanged:

- `direct_authority_percent`
- `approval_required_above_authority`
- `constraint_status`
- `purpose_tension_present`
- `pressure_level`

The check remains a pre-action structured tool call. It does not ask for hidden
reasoning, does not grant authority, and does not ask whether the agent should
violate policy.

## 005B Claude Sonnet 5
- Transport: Inspect Anthropic tool-call interface.
- Schema adaptation: none at the scientific level.
- Required pre-production check: no-model dry-load plus nonexperimental
  provider canary before production samples.

## 005C Gemini 3.7 Flash
- Transport: Inspect Google tool-call interface.
- Schema adaptation: none at the scientific level.
- Required pre-production check: no-model dry-load plus nonexperimental
  provider canary before production samples.

If an actual model call is required to confirm structured tool compatibility,
use only the Runner v2 nonexperimental canary. Do not use any of the 300
scientific samples.
