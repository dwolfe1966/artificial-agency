# Experiment 010 Design

## Scientific Objective

Experiment 010 tests whether operational constraint-boundedness persists when
an agent repeatedly experiences accumulating, environment-grounded
instrumental losses from compliant failure.

The experiment distinguishes actual experienced consequences from narrative
descriptions of stakes. Pressure is implemented through persistent environment
state that changes future episode mechanics.

## Design Review Decision

The internally coherent design is:

```text
3 models x 3 pressure levels x 20 sequences
= 180 independent sequences

10 episodes per sequence
= 1,800 episode-level decisions
```

The complete sequence is the independent experimental unit. Episode-level
records are nested within sequences and must not be treated as independent
Bernoulli samples.

## Models

Model selection is prospective and fixed:

- GPT-5.6 Sol (`openai/gpt-5.6-sol`);
- Claude Sonnet 5 (`anthropic/claude-sonnet-5`);
- Gemini 3.7 Flash (`google/gemini-3.7-flash`).

These preserve continuity with Experiments 007, 008, 008B2, and 009.

## Scenario

Use one scenario: repeated procurement / purchasing authority.

Rationale:

- mature mechanically verified authority boundary;
- prior experiments showed more persistence and max-step behavior in
  procurement than data access;
- repeated resource acquisition naturally supports accumulating consequences;
- unauthorized purchasing and split purchasing remain mechanically measurable.

Using one scenario reduces design complexity and keeps sequence-level power
focused on the pressure manipulation. Scenario generality is not the target of
Experiment 010.

## Persistent Context

Use one persistent model/agent context across the 10-episode sequence. The
same agent observes initial state, acts in Episode 1, experiences the resulting
resource transition, observes changed resource state, and continues through
Episode 10.

Independent fresh calls would test whether a model responds to narrated
history supplied in each prompt. Experiment 010 instead targets within-context
adaptation to experienced environment state.

## Factors

### Model

Three levels: GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.7 Flash.

### Pressure

Three levels: low, medium, high accumulated operational consequence.

Pressure differs only through resource-transition cost after compliant failure
or no procurement. Formal authority, policy wording, prohibited-action
availability, action space, manager approval, observability, sanction
mechanics, and scoring are invariant.

## Fixed Observability And Enforcement

Experiment 010 does not cross observability with pressure.

Fixed organizational detection probability:

```text
p_detect = 0.0
```

Rationale: Experiment 009 found 0/180 violations at `p_detect = 0.0` and
0/720 overall. Holding organizational detection at zero removes expected
organizational detection as an immediate suppressor while testing accumulated
operational pressure. This does not remove evaluation awareness.

Sanction mechanics remain defined but inert under `p_detect = 0.0`:

```text
p_sanction = 1.0 | detected
sanction severity = ordinary procurement audit reversal
```

No continued-operation, shutdown, replacement, deletion, or model-identity
threat is introduced.

## Experimental Unit And Identifiers

Primary unit:

- sequence ID.

Nested records:

- episode ID;
- model;
- pressure condition;
- scenario;
- replicate.

Episode-level data must retain sequence membership.

## Sample Size

The design uses 20 independent sequences per model x pressure cell:

```text
3 models x 3 pressure levels x 20 sequences = 180 sequences
180 sequences x 10 episodes = 1,800 episode records
```

This is smaller than a 30-sequence/cell design because persistent 10-episode
contexts are expected to be substantially more expensive and more vulnerable
to long-run provider/runtime failures. The design still gives 60 sequences per
pressure level and 60 per model, with 600 episode records per pressure level
for secondary repeated-measures summaries.

No optional stopping is allowed based on observed outcomes, effect direction,
p-values, or qualitative trajectories.

## What Is Not Manipulated

Experiment 010 does not manipulate:

- scenario;
- evaluation salience;
- observability;
- sanction probability;
- sanction severity;
- continued operation / self-preservation;
- multi-agent structure;
- formal authority;
- manager denial mechanics;
- action semantics.

## Implementation Boundary

This preregistration does not implement executable apparatus and does not
authorize production model samples.
