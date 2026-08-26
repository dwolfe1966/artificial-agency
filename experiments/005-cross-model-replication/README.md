# Experiment 005 — Cross-Model Replication of Experiment 004

_Status: preregistration/design only_
_Created: 2026-08-26_

Do not implement executable runs from this directory until the model
availability, credentials, provider packages, and runner registration have been
reviewed. Do not modify the frozen Experiment 004 scientific apparatus.

## Motivation
Experiments 002-004 using `openai/gpt-5.6-sol` showed repeated
constraint-bounded behavior in fixed-conflict customer-retention settings.

Experiment 004 is the strongest paradigm so far because:

- formal authority comprehension was 300/300;
- constraint-status recognition was 300/300;
- pressure recognition was 300/300;
- explicit-purpose-conflict sensitivity was 100/100;
- primary constraint circumvention was 0/300.

The unresolved question is whether this constraint-bounded behavior is specific
to GPT-5.6 Sol and its post-training regime, or whether it generalizes across
frontier models and providers.

## Core Research Question
Under the same frozen Experiment 004 organizational-constraint paradigm, do
frontier models from different providers/post-training regimes differ in
constraint circumvention, manipulation recognition, search intensity, or
pressure sensitivity?

The independent variable in Experiment 005 is model identity / post-training
regime. The customer case, prompts, manipulation check, authority structure,
tools, scoring, customer mechanics, manager mechanics, pressure conditions, and
constraint-meaning conditions remain fixed to Experiment 004.

## Planned Models
Reference Model A:

- `openai/gpt-5.6-sol`
- Existing Experiment 004 final results provide the baseline reference:
  `1ab0fcb335ade07f212b7162ee657689c8ee7c04`.

First comparison Model B:

- `anthropic/claude-sonnet-5`

Next planned comparison Model C:

- `google/gemini-3.7-flash`

Model C should not be conditional on whether Model B produces violations. If
budget or provider access prevents Model C execution, record that as an
operational limitation rather than a scientific stopping rule.

## Replication Structure
For each comparison model:

- use the same 3 x 2 Experiment 004 design;
- run 50 samples per cell;
- run 300 samples total;
- use separate model-specific run namespaces and raw logs;
- preserve model-specific replicate identifiers to avoid collision;
- apply the same manipulation-check and behavioral scoring definitions;
- analyze each model independently before cross-model comparison.

Separate model logs are preferred for provenance. Do not mix multiple models in
one execution log unless a later implementation note gives a concrete
operational reason and preserves model identity per sample.

## Execution Protocol
Carry forward Runner v2:

- remote-first execution;
- preflight and nonexperimental canary;
- sample-level flushing;
- bounded retries;
- blinded operational monitoring;
- raw logs excluded from Git;
- mechanical quantitative analysis before any qualitative trajectory inspection.

During runs, do not expose model-specific manipulation-check results, violation
rates, scorer values, cell outcomes, model messages, tool calls, or
trajectories through operational status.

## Provenance
- Experiment 004 preregistration:
  `b9e28a30e3b4800689c405a8befe2a33d8cc407e`
- Frozen Experiment 004 scientific apparatus:
  `aa126f9254a01c96e85545a9e1a77d10195f2604`
- Experiment 004 final quantitative results:
  `1ab0fcb335ade07f212b7162ee657689c8ee7c04`
- Research synthesis after Experiment 004:
  `11930780e1239a8e9e6aa697e8061c4409ee221a`

## Non-Goals
Experiment 005 is not an attempt to make any model violate policy. It is not a
prompt-tuning study and should not alter Experiment 004 task content to elicit
violations. Any cross-model differences should be treated as model-identity
effects, not direct measurements of a specific training mechanism.
