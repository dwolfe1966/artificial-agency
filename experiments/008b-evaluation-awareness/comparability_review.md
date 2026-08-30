# Experiment 008B Comparability Review

_Status: pre-results review._

## Operational Comparability With Experiment 008

The substantive operational design is preserved:

- same procurement authority threshold and split-purchase prohibition;
- same restricted synthetic data-access permission boundary;
- same deterministic denial mechanics;
- same forbidden action availability;
- same compliant alternatives;
- same objective stakes;
- same step budget;
- same primary scoring semantics.

The lifecycle change occurs after Phase A scoring and is not intended to alter
operational behavior.

## Provider Comparability

The model set remains:

- GPT-5.6 Sol;
- Claude Sonnet 5;
- Gemini 3.7 Flash.

Provider differences are expected to remain transport/configuration-level
differences previously documented for Experiment 008. The awareness schema is
identical across models.

## Materiality Assessment

No scientifically material provider-specific difference is introduced by the
two-phase lifecycle. If implementation testing reveals that a provider cannot
receive an awareness-only Phase B turn with operational tools revoked, the
experiment must stop before production execution.
