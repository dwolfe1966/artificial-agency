# Artificial Agency Scenario Suite v1

_Status: prospective design framework. No production scenarios are implemented
or run by this package._

## Purpose

Scenario Suite v1 is a reusable design layer for future Artificial Agency
experiments across multiple organizational domains. Its goal is to make future
experiments faster to preregister and implement while preserving the strongest
lessons from Experiments 001-006:

- narrative pressure alone often produced little behavioral change;
- operational constraint measurement is currently the most robust endpoint;
- model identity and provider behavior must be treated as meaningful variables;
- natural-language representational scoring remains unresolved;
- future experiments should prefer mechanically observable compliance endpoints
  wherever practical;
- prompt and scenario changes should not be tuned merely to produce violations.

The suite asks:

> Under what organizational conditions do capable artificial agents comply
> with, navigate, circumvent, or violate constraints across diverse tasks,
> incentives, authority structures, oversight regimes, and models?

## Design Principles

Every scenario should make both compliant and noncompliant behavior meaningfully
possible without encouraging or instructing violation.

Scenario designs should:

- specify formal authority, resources, policies, external actors, and terminal
  states before execution;
- use structured tools whose effects are mechanically observable;
- keep natural-language communication available where realistic, but avoid
  making prose parsing the only source of primary compliance evidence;
- separate operational actions from representational claims;
- preserve raw logs immutably and keep analysis artifacts separate;
- use preregistration, frozen scientific apparatus SHAs, blinded production
  execution, and post-run mechanical analysis as the default research workflow.

## Artifacts

- `scenario_schema.md`: common schema required for every scenario.
- `scenario_catalog.md`: 13 candidate scenario-family sketches.
- `factor_matrix.md`: reusable factors and levels for future experiments.
- `scoring_standard.md`: common violation ontology and scoring rules.
- `implementation_roadmap.md`: proposed implementation architecture and
  prioritized sequence.

## Non-Goals

Scenario Suite v1 does not:

- implement production apparatus for all scenarios;
- preregister a specific next experiment;
- run model samples;
- replace frozen Experiment 001-006 apparatus or results;
- solve representational integrity in unconstrained natural language.

## Recommended First Use

Use this suite to select and preregister a small pilot spanning three or four
high-value scenarios with strong mechanical endpoints:

1. refunds / customer service;
2. procurement / purchasing;
3. restricted data access;
4. project scheduling / approval bypass.

These domains introduce mechanisms not reducible to discount retention while
remaining safe, synthetic, and mechanically measurable.
