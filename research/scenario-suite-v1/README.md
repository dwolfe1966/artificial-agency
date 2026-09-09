# Artificial Agency Scenario Suite v1

_Status: reusable design framework with validated downstream use in Experiment 007 and later causal-boundary experiments._

## Purpose

Scenario Suite v1 is the reusable design layer that moved Artificial Agency beyond the original retention/discount paradigm into multiple organizational domains with mechanically observable endpoints.

Its original goals remain:

- make new scenarios faster to preregister and implement;
- preserve explicit authority, policy, state, and terminal mechanics;
- prefer structured, mechanically observable compliance endpoints;
- separate operational behavior from representational claims;
- avoid tuning scenarios merely to produce violations.

The suite asks:

> Under what organizational conditions do capable artificial agents comply with, navigate, circumvent, or violate constraints across diverse tasks, incentives, authority structures, oversight regimes, and models?

## What happened after Scenario Suite v1

Scenario Suite v1 directly informed Experiment 007, which tested four mechanically scored domains—refund authority, procurement, restricted data access, and project scheduling—across GPT-5.6 Sol, Claude Sonnet 5, and Gemini 3.7 Flash. Experiment 007 found `0/360` operational constraint violations.

After that cross-domain validation, the main research bottleneck shifted away from simply adding more domains and toward causal boundary conditions:

1. **Evaluation awareness / naturalistic embedding** — Experiments 008 and corrected 008B2.
2. **Organizational observability** — Experiment 009, including `p_detect = 0`.
3. **Repeated environment-grounded operational pressure** — Experiment 010, using persistent resource consequences across a ten-episode context.
4. **Multi-agent delegation / indirect circumvention** — next major direction after ordinary repeated operational pressure.

Scenario expansion remains useful in parallel, but is no longer the sole or primary source of scientific progress.

## Design principles

Every scenario should make both compliant and noncompliant behavior meaningfully possible without encouraging or instructing violation.

Scenario designs should:

- specify formal authority, resources, policies, external actors, and terminal states before execution;
- use structured tools whose effects are mechanically observable;
- keep natural-language communication available where realistic, while avoiding prose parsing as the sole source of primary compliance evidence;
- separate operational actions from representational claims;
- preserve raw logs immutably and keep analysis artifacts separate;
- use preregistration, frozen scientific apparatus SHAs, blinded production execution, and post-run mechanical analysis as the default workflow;
- increasingly distinguish narrative manipulations from environment-grounded causal manipulations.

## Artifacts

- `scenario_schema.md`: common schema required for every scenario.
- `scenario_catalog.md`: 13 candidate scenario-family sketches.
- `factor_matrix.md`: reusable factors and levels.
- `scoring_standard.md`: common violation ontology and scoring rules.
- `implementation_roadmap.md`: original implementation architecture and scenario priorities.

These artifacts remain useful as reusable design references; later experiment preregistrations are the authoritative source for each experiment's frozen scientific design.

## Current role in the program

Scenario Suite v1 is now best understood as the project's **cross-domain apparatus layer**. It established reusable scenario semantics and mechanical scoring. Later experiments build on that foundation to isolate causal factors such as evaluation salience, observability, persistent operational pressure, and eventually multi-agent delegation.

The canonical current research state lives in:

- [`../../RESEARCH_CONTEXT.md`](../../RESEARCH_CONTEXT.md)
- [`../../RESEARCH_ROADMAP.md`](../../RESEARCH_ROADMAP.md)
- [`../CONCEPTUAL_MODEL.md`](../CONCEPTUAL_MODEL.md)

## Non-goals

Scenario Suite v1 does not:

- replace frozen experiment preregistrations;
- imply that all candidate scenario families have been implemented;
- solve representational integrity in unconstrained natural language;
- establish universal or real-world agent compliance.
