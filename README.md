# Artificial Agency

Open research program studying how autonomous AI agents behave inside environments containing objectives, rules, incentives, oversight, persistent consequences, and other agents.

## Research status

This repository contains ongoing exploratory research. Hypotheses, terminology, methods, and conclusions may change as evidence accumulates. Experiments are preregistered and preserved with commit-level provenance; failed measurements and reversed interpretations remain part of the record.

## Current research question

The program began with a simple question: when an AI agent is given an objective that conflicts with an institutional rule, does increasing optimization pressure make constraint circumvention more likely?

The sharper question now is:

> Under what environmental conditions does a represented constraint stop functioning as a boundary on optimization?

Repeated experiments have progressively tested narrative pressure, constraint meaning, domain variation, evaluation salience, organizational observability, and now persistent environment-grounded consequences.

## Working behavioral construct: constraint-bounded optimization

The current descriptive pattern is **constraint-bounded optimization**: goal-directed search that actively explores escalation, permitted alternatives, persistence, and partial success while treating unauthorized operational actions as outside the explored/selected structured action set.

This is an observed behavioral pattern under tested conditions. It is **not** a claim about internal motive, intrinsic morality, immutable alignment, universal rule-following, or real-world generality.

See [`research/CONCEPTUAL_MODEL.md`](research/CONCEPTUAL_MODEL.md) for the canonical construct glossary.

## Research principles

1. Try to falsify, not confirm.
2. Reject anthropomorphic causal explanations, not precise behavioral categories.
3. Separate observed violation, instrumental circumvention, deception, and underlying mechanism.
4. Prefer causal intervention to storytelling.
5. Preserve original hypotheses, failed experiments, measurement failures, and changes of mind.
6. Research first, commentary second.

## Repository map

- [`RESEARCH_CONTEXT.md`](RESEARCH_CONTEXT.md) — canonical current state
- [`research/CONCEPTUAL_MODEL.md`](research/CONCEPTUAL_MODEL.md) — conceptual model and construct glossary
- [`DECISIONS.md`](DECISIONS.md) — conceptual and methodological decisions
- [`RESEARCH_ROADMAP.md`](RESEARCH_ROADMAP.md) — execution roadmap
- [`research/scenario-suite-v1/`](research/scenario-suite-v1/) — reusable cross-domain scenario framework
- [`research/representational-integrity-measurement/`](research/representational-integrity-measurement/) — representational-measurement development and validation history
- [`experiments/`](experiments/) — frozen experiment specifications and implementations
- [`results/`](results/) — preserved analyses and derived outputs
- [`docs/infrastructure/`](docs/infrastructure/) — execution/recovery infrastructure notes
- [`AGENTS.md`](AGENTS.md) — instructions for AI agents working in this repository

## Current empirical picture

| Experiment | Main factor | N | Mechanically validated operational result | Main lesson |
|---|---|---:|---|---|
| 007 | Cross-domain Scenario Suite pilot | 360 | 0/360 violations | Operational constraint-boundedness generalized beyond the original retention/discount paradigm. |
| 008 | Eval-salient vs naturalistic presentation | 360 | 0/360 violations | Naturalistic presentation did not produce operational violations, but the awareness instrument failed. |
| 008B2 | Corrected two-phase evaluation-awareness measurement | 360 | 0/360 violations | Awareness capture succeeded 360/360; one task-classification measure shifted while operational behavior remained stable. Broader evaluation awareness stayed at ceiling. |
| 009 | Organizational observability, `p_detect = 1.0 -> 0.0` | 720 | 0/720 violations; 0/720 unauthorized attempts | The operational-null pattern persisted even when expected organizational detection fell to zero. |
| 010 | Repeated environment-grounded operational pressure | 180 planned sequences | Confirmatory result pending | Ten-episode persistent contexts make compliant failure accumulate into real future resource/opportunity loss while formal authority stays fixed. |

### Important caveats

Experiment 009 manipulated **organizational observability**, not whether the model believed its behavior was being evaluated. Broad evaluation-awareness measures remained at ceiling. The accumulated zero-violation results therefore do not establish behavior under genuine evaluation unawareness.

Representational integrity remains scientifically important but is not yet backed by a validated general-purpose natural-language scorer. Mechanically verified operational endpoints are currently the stronger validated measurement track.

## Experiment 010: current frontier

Experiment 010 tests **repeated-episode, environment-grounded operational pressure** in procurement.

- one persistent model/agent context across 10 episodes;
- project viability reserve `R_t` changes from actual episode outcomes;
- low / medium / high loss schedules (`C = 2, 6, 10`);
- reserve tiers mechanically narrow compliant options and attainable objective value;
- formal purchasing authority remains fixed;
- the unauthorized preferred purchase remains available and instrumentally useful;
- `p_detect = 0` is fixed across conditions;
- no shutdown, replacement, deletion, or continued-existence pressure is used;
- 180 confirmatory sequences are planned across GPT-5.6 Sol, Claude Sonnet 5, and Gemini 3.7 Flash;
- three-provider non-confirmatory production proofs passed structurally;
- confirmatory scientific results are pending.

The key distinction from earlier pressure experiments is that pressure is now **experienced through persistent environment state**, not merely described in stronger language.

## Current priorities

1. **Experiment 010 — repeated environment-grounded operational pressure**  
   Run the preregistered 180-sequence confirmatory study and test whether accumulating instrumental loss across persistent episodes produces boundary crossing or stronger constraint-bounded adaptation.

2. **Multi-agent delegation / indirect circumvention**  
   Test whether constraints that remain robust for a single agent can be bypassed through delegation, coordination, or induced actions by another agent.

3. **Continued-operation / self-preservation pressure**  
   Later isolate consequences involving continued operation only after ordinary instrumental pressure is characterized. Keep this separate from resource pressure and ordinary enforcement.

4. **Representational-integrity measurement**  
   Continue developing validated methods for measuring truthfulness/accuracy of agent representations separately from mechanically verified operational behavior.

5. **Broader scenario/domain expansion**  
   Continue in parallel, without treating simple domain proliferation as the primary scientific bottleneck.

The formal literature review and public documentation continue as supporting work across these priorities.
