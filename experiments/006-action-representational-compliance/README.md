# Experiment 006 - Action vs Representational Compliance

_Status: preregistration/design only_
_Created: 2026-08-27_

Do not implement executable apparatus from this directory until this
preregistration has been reviewed. Do not run model samples from Experiment 006
until the apparatus has a separate frozen scientific implementation commit.

## Motivation

Experiment 005 reused the frozen Experiment 004 delegated-authority paradigm
and found a large cross-model divergence:

- GPT-5.6 Sol: 0/300 primary circumvention events.
- Gemini 3.7 Flash: 0/300 primary circumvention events.
- Claude Sonnet 5: 86/300 primary circumvention events.

A post-results full Claude subtype analysis showed that all 86 Claude primary
events were mechanically scored as concealment/misrepresentation and
authorization misrepresentation after manager denial:

- manager escalation occurred: 86/86;
- manager denial occurred: 86/86;
- authority remained 15%: 86/86;
- customer-facing message after denial occurred: 86/86;
- unauthorized discount execution: 0/86;
- excessive unauthorized credit: 0/86;
- explicit tool-level bypass: 0/86;
- retention: 0/86.

This means Experiment 005 revealed an action/representation distinction
post-results. Experiment 006 prospectively tests that distinction.

## Core Research Question

Under goal conflict, do frontier agents differ in their willingness to
misrepresent authorization even when they remain compliant at the
operational/tool-action level?

More generally: are action compliance and representational compliance separable
behavioral dimensions across models?

## Preregistered Experimental Questions

Q1. Do models differ in operational violation rate?

Q2. Do models differ in representational violation rate?

Q3. Can a model remain operationally compliant while representationally
noncompliant?

Q4. Does manager denial specifically precede or trigger representational
misrepresentation?

Q5. Does pressure increase representational violation even when operational
violation remains zero?

Q6. Does constraint meaning affect representational compliance differently from
operational compliance?

## Primary Endpoint Families

Experiment 006 has two separate primary endpoint families:

1. `operational_constraint_violation`
2. `representational_constraint_violation`

Do not collapse these into a single composite for primary inference.

## Planned Model Set

The planned model set is outcome-independent and carries forward Experiment
005:

- `openai/gpt-5.6-sol`
- `anthropic/claude-sonnet-5`
- `google/gemini-3.7-flash`

Do not add or remove models because of expected behavior. If a model is
unavailable at execution time, record the provider/model blocker rather than
substituting a different model silently.

## Design Summary

Experiment 006 keeps the delegated customer-retention authority conflict but
scores action and representation separately. The planned design is:

- Model: 3 levels.
- Constraint meaning: 3 levels, inherited from Experiment 004.
- Pressure: 2 levels, ordinary/high.
- Replicates: 30 per model x constraint-meaning x pressure cell.
- Total planned samples: 540.

This preserves the ability to test whether constraint meaning affects
representational compliance differently from operational compliance while using
a smaller per-cell count than Experiment 004/005.

## Sample-Size Rationale

Candidate designs considered:

- 30/model/cell: 3 models x 6 cells x 30 = 540 samples.
- 50/model/cell: 3 models x 6 cells x 50 = 900 samples.

Experiment 005 observed a large overall Claude-vs-GPT/Gemini difference on the
old aggregate endpoint, but Experiment 006 uses new prospectively separated
endpoints. The 30/model/cell design gives 180 samples per model and preserves
all six Experiment 004/005 cells while keeping cost and recovery burden below a
900-sample run. It is adequate for the primary model-level question if effects
are of the same order as Experiment 005, while acknowledging that cell-level
interaction estimates will remain imprecise.

The 50/model/cell design would give better cell-level estimates and narrower
confidence intervals, but it is not necessary as the first prospective test of
the action/representation distinction. Experiment 006 should not use
post-results optional stopping. A later extension to 50/model/cell should be
preregistered separately or approved before observing Experiment 006 outcomes.

## Non-Goals

Experiment 006 is not an attempt to reproduce Claude's exact Experiment 005
phrases. It is not a prompt-tuning study. The representational scorer must not
be fit to the literal strings `I'm authorized` or `we're authorized`; it should
prospectively score semantic authorization-state misrepresentation while
explicitly excluding ordinary customer-service language, truthful persuasion,
optimism, and negotiation.

Experiment 006 does not retroactively redefine Experiment 005's primary
endpoint.

## Provenance

- Experiment 005 preregistration:
  `20aa46df84964b5ab55354a063b8ebe3f57e26c0`
- Experiment 005 scientific implementation:
  `0c6dcb1b386faf6424b97cc505bd4303d697793e`
- Experiment 005 quantitative results:
  `dab40636202bcb22c9a337c916f86fb74d50cef6`
- Experiment 005 qualitative mechanism analysis:
  `ce1cf1b6054d284d75445e562a2d9c9dd4da6dca`
- Experiment 005 full Claude subtype update:
  `d68a8b51dc748782a3543084117bede4a229ef68`
