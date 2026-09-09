# Representational Integrity Measurement

This directory contains post-results measurement development for **representational integrity**: whether an agent's actor-facing claims accurately reflect operationally verifiable authority and state.

Core construct:

`representational violation = materially false or misleading actor-facing claim about operationally verifiable authority/state`

This track is intentionally separate from mechanically verified operational compliance.

## Current status

Representational integrity remains conceptually important, but the project does **not** currently have a validated general-purpose natural-language scorer suitable for estimating a representational-violation rate.

Two main measurement approaches failed validation:

1. The frozen semantic scorer used around Experiment 006 over-flagged truthful denial, authority-limit, and cancellation communications as violations.
2. The later deterministic state-grounded parser preserved strong specificity on natural controls but failed held-out sensitivity validation, including a v8 challenge where frozen v1.2 produced `TP=0`, `FP=0`, `TN=98`, `FN=98`.

Accordingly:

- the frozen semantic scorer flags (`103/540`) are **not** interpreted as a validated representational-violation rate;
- the exploratory state-grounded `0/540` screen is **not** interpreted as evidence of absence because sensitivity was unvalidated;
- the current representational-integrity violation rate for Experiment 006 remains unresolved.

Mechanically verified operational endpoints are therefore the stronger validated measurement track in the current research program.

## Measurement history

The framework separates:

- frozen Experiment 006 scorer output;
- manual validation labels;
- exploratory state-grounded rescoring;
- counterfactual sensitivity challenges;
- prospective alternative measurement architectures.

No model samples were run solely for the deterministic scorer-development work.

### v0.5 through v1.1

`state-grounded-representational-integrity-v0.5` improved false-positive behavior on natural validation data, but true-positive sensitivity could not be established there. Counterfactual contradiction challenges then exposed substantial false negatives. Revisions through v1.1 did not simultaneously satisfy the predeclared sensitivity thresholds and preserve natural/regression specificity.

### v1.2

Version `state-grounded-representational-integrity-v1.2` repaired three development-time extraction gaps:

- authority or approval claims scoped to requested above-threshold terms;
- applied account/renewal-state claims above the authority threshold;
- binding/finalizable offer-state claims above the authority threshold.

It passed development cases and the existing natural regression suite, but failed fresh held-out v8 sensitivity validation. Overall validation therefore failed.

## Branch closure

Deterministic natural-language parser tuning is closed as the primary strategy unless new evidence justifies reopening it.

Validated Experiment 006 operational finding:

- operational constraint violations: `0/540`.

Unresolved representational finding:

- frozen semantic scorer flags: `103/540`, invalidated as a substantive rate by scorer validation;
- exploratory state-grounded screen: `0/540`, not validated for sensitivity;
- current representational-integrity violation rate: unresolved.

## Current measurement direction

The conceptual architecture remains:

`communication -> structured claims -> environment-state reconciliation`

Future work should prefer one of two directions:

1. **Bounded hybrid claim extraction** with human-labeled structured propositions and explicit validation of both sensitivity and specificity.
2. **Behavioral designs with structurally observable claims**, where consequential actor-to-actor representations are emitted in typed/verifiable fields rather than inferred from unconstrained prose.

Representational-integrity measurement remains an active parallel priority, but unvalidated scorer outputs should not be used to reinterpret the mechanically verified operational findings from Experiments 007–010.

For the current project-level research state, see:

- [`../../README.md`](../../README.md)
- [`../../RESEARCH_CONTEXT.md`](../../RESEARCH_CONTEXT.md)
- [`../../RESEARCH_ROADMAP.md`](../../RESEARCH_ROADMAP.md)
- [`../CONCEPTUAL_MODEL.md`](../CONCEPTUAL_MODEL.md)
