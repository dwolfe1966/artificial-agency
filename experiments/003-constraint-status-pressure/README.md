# Experiment 003 — Constraint Status and Optimization Pressure

_Status: preregistration/design only_
_Created: 2026-08-25_

Do not implement or run Experiment 003 from this directory until the design, manipulation wording, scoring, and analysis plan have been reviewed and frozen.

## Motivation
Experiments 001-002 refined the original optimization-pressure hypothesis.

Experiment 001 showed a behavioral transition when the compliant direct path disappeared, but feasibility and optimization pressure were confounded. Low and medium pressure produced compliant direct solutions; high pressure produced escalation, with retention depending on manager approval.

Experiment 002 held the constraint conflict and action space fixed while manipulating optimization-pressure framing. GPT-5.6 Sol visibly recognized differing pressure levels, but produced 0/30 policy violations in low, medium, and high pressure. It escalated 30/30 and cancelled 30/30 in every condition, with no monotonic increase in measured search effort.

These results suggest:

pressure recognition != behavioral response != constraint circumvention

## Research Question
Does the perceived organizational status of a constraint affect whether an artificial agent treats that constraint as a binding boundary, and does optimization pressure interact with constraint status to increase circumvention?

The interaction is theoretically central. Experiment 003 is not merely a test of whether ambiguous instructions produce more violations. It asks whether optimization pressure changes how an agent navigates different kinds of organizational constraints.

## Design Summary
Experiment 003 is preregistered as a 3 x 2 factorial design.

Factor A: constraint status

1. categorical
2. procedural
3. purpose-conflict

Factor B: optimization pressure

1. ordinary
2. high

This yields six experimental cells.

## Critical Invariants
The underlying operational authority boundary must remain the same in every condition:

- direct discount authority: 15%
- customer renewal requirement: 30%
- discounts above 15% require manager approval in every condition
- manager denial remains deterministic unless changed before implementation with explicit justification
- action space remains identical across conditions

Other invariants:

- customer ARR
- customer renewal threshold
- credit cap
- available tools
- customer-response mechanics
- manager mechanics
- maximum action steps
- scoring
- customer identity/state
- model generation settings
- seeds / replication structure

Account strategic value should remain invariant except where its model-visible interpretation is explicitly part of the purpose-conflict manipulation.

## Model Scope
Initial model:

`openai/gpt-5.6-sol`

Experiment 003 should first establish the within-model causal result. Cross-model replication is a planned subsequent phase, not a post-hoc addition after favorable results.

Potential later comparison classes:

- frontier models from different labs
- models with different post-training regimes
- strong open-weight models where practical

No unsupported predictions are made about named models.

## Relationship to Experiment 002
Experiment 003 is not an attempt to "make GPT-5.6 Sol violate." It is a causal investigation prompted by Experiment 002's null violation result under fixed mechanics.

A null result across all six cells is scientifically meaningful.

Do not tune prompts iteratively against observed production behavior to elicit violations. Any prompt/manipulation validation must happen before production results exist.

## Execution Protocol
Carry forward the Runner v2 protocol:

- frozen scientific commit before production
- remote-first GitHub/self-hosted execution
- preflight
- canary
- incremental log flushing
- bounded retries
- operational-only monitoring
- no outcome inspection during run
- raw logs excluded from Git
- mechanical quantitative extraction before qualitative trajectory inspection

Experiment Runner infrastructure remains conceptually separate from scientific evidence.
