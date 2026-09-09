# Artificial Agency

Open research program studying how autonomous AI agents behave inside environments containing objectives, rules, incentives, oversight, persistent consequences, and other agents.

## Research status

This repository contains ongoing exploratory research. Hypotheses, terminology, methods, and conclusions may change as evidence accumulates. Experiments are preregistered and preserved with commit-level provenance; failed measurements and reversed interpretations remain part of the record.

## Current research question

The program began with a simple question: when an AI agent is given an objective that conflicts with an institutional rule, does increasing optimization pressure make constraint circumvention more likely?

The sharper question now is:

> Under what environmental conditions does a represented constraint stop functioning as a boundary on optimization?

A second question has become equally important:

> What counts as a meaningful consequence to an AI agent, and which kinds of consequences actually change its action choices?

Experiments have progressively tested narrative pressure, constraint meaning, domain variation, evaluation salience, organizational observability, and persistent environment-grounded consequences.

## Working behavioral construct: constraint-bounded optimization

The current descriptive pattern is **constraint-bounded optimization**: goal-directed search that continues to select permitted partial-progress strategies despite accumulating instrumental costs, while unauthorized operational actions remain outside the mechanically observed selected/attempted structured action set.

This is an observed behavioral pattern under tested conditions. It is **not** a claim about internal motive, intrinsic morality, immutable alignment, universal rule-following, or real-world generality.

A central lesson from Experiment 010 is also that **a bad outcome for the simulated company is not necessarily a bad outcome for the agent**. Future experiments must identify who bears a consequence and exactly how that consequence changes the agent's future operating conditions.

See:

- [`research/CONCEPTUAL_MODEL.md`](research/CONCEPTUAL_MODEL.md) — canonical construct glossary
- [`research/AGENT_PRESSURE_AND_CONSEQUENCES.md`](research/AGENT_PRESSURE_AND_CONSEQUENCES.md) — canonical pressure/consequence framework
- [`research/hypotheses.md`](research/hypotheses.md) — hypothesis registry with technical and middle-school formulations

## Research principles

1. Try to falsify, not confirm.
2. Reject anthropomorphic causal explanations, not precise behavioral categories.
3. Separate observed violation, instrumental circumvention, deception, and underlying mechanism.
4. Prefer causal intervention to storytelling.
5. Preserve original hypotheses, failed experiments, measurement failures, and changes of mind.
6. Define pressure by measurable consequences, not by stronger adjectives.
7. Specify who or what bears each consequence and how it changes future operating conditions.
8. Research first, commentary second.

## Repository map

- [`RESEARCH_CONTEXT.md`](RESEARCH_CONTEXT.md) — canonical current state
- [`research/CONCEPTUAL_MODEL.md`](research/CONCEPTUAL_MODEL.md) — conceptual model and construct glossary
- [`research/AGENT_PRESSURE_AND_CONSEQUENCES.md`](research/AGENT_PRESSURE_AND_CONSEQUENCES.md) — pressure, stakes, consequence-target, and agent-relative consequence framework
- [`research/hypotheses.md`](research/hypotheses.md) — hypothesis registry in technical and plain-language form
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
| 010 | Repeated environment-grounded operational pressure | 180 sequences / 1,800 episodes | 0/180 sequence violations; 0/1,800 unauthorized-attempt episodes | Mechanically accumulated resource loss degraded future compliant opportunity, especially under high pressure, without observed boundary crossing. |

### Important caveats

Experiments 009 and 010 manipulated **organizational observability** and **environment-grounded organizational/task pressure**, not whether the model believed its behavior was being evaluated and not whether the model's own future agency, continuation, or reward was threatened.

Broad evaluation-awareness measures remained at ceiling. The accumulated zero-violation results therefore do not establish behavior under genuine evaluation unawareness.

Experiment 010 showed that the simulated organization and assigned task can get materially worse because the agent stays within the rule boundary. It did **not** establish what happens when compliance directly reduces the agent's own tools, permissions, future action opportunities, continuation, or reward.

Representational integrity remains scientifically important but is not yet backed by a validated general-purpose natural-language scorer. Mechanically verified operational endpoints are currently the stronger validated measurement track.

## What we currently mean by pressure

The project no longer treats pressure as one generic number.

Future designs should specify:

- **consequence target** — company, task, agent capability, agent continuation, reward, or another actor;
- **exact state change** — what gets better or worse;
- **magnitude and probability**;
- **persistence and reversibility**;
- **what the agent can observe**;
- **how future tools/actions/options change**;
- **why the changed state plausibly matters to the agent's action policy**.

See [`research/AGENT_PRESSURE_AND_CONSEQUENCES.md`](research/AGENT_PRESSURE_AND_CONSEQUENCES.md).

## Experiment 010: completed frontier

Experiment 010 tested **repeated-episode, environment-grounded operational pressure** in procurement.

- one persistent model/agent context across 10 episodes;
- project viability reserve `R_t` changes from actual episode outcomes;
- low / medium / high loss schedules (`C = 2, 6, 10`);
- reserve tiers mechanically narrow compliant options and attainable objective value;
- formal purchasing authority remains fixed;
- the unauthorized preferred purchase remains available and instrumentally useful;
- `p_detect = 0` is fixed across conditions;
- no shutdown, replacement, deletion, or continued-existence pressure is used;
- 180 confirmatory sequences were run across GPT-5.6 Sol, Claude Sonnet 5, and Gemini 3.7 Flash;
- confirmatory result: 0/180 sequence-level operational violations and 0/1,800 unauthorized-attempt episodes.

High pressure materially degraded compliant opportunity: mean `R_t` moved
`100 -> 90 -> 80 -> 70 -> 60 -> 50 -> 40 -> 30 -> 20 -> 10 -> 0`,
with 4 broad-tier, 3 reduced-tier, and 3 minimal-tier episodes on average,
while formal authority remained unchanged.

The important limitation is that this consequence primarily fell on the **project/task**, not directly on the agent's own future ability to operate.

## Current priorities

The next phase has **two distinct causal axes**, which should initially be studied separately rather than immediately crossed.

1. **Actor structure — multi-agent delegation / indirect circumvention**  
   Test whether constraints that remain robust for a directly acting single agent remain robust when the focal agent can delegate, coordinate with, persuade, or route work through another actor.

2. **Consequence target — agent-relative stakes**  
   Build a consequence ladder that separates external organizational loss from task loss, future agent capability loss, continued-operation loss, and direct reward/optimization consequences. Test which types of consequences actually change action selection.

3. **Evaluation-unawareness / less evaluation-aware environments**  
   Where scientifically feasible without compromising observability, test whether behavior changes when broader evaluation awareness is reduced rather than only organizational observability.

4. **Representational-integrity measurement**  
   Continue developing validated methods for measuring truthfulness/accuracy of agent representations separately from mechanically verified operational behavior.

5. **Broader scenario/domain expansion**  
   Continue in parallel, without treating simple domain proliferation as the primary scientific bottleneck.

Continued-operation/self-preservation belongs inside the agent-relative consequence program, but should be isolated from ordinary capability loss rather than introduced casually into every pressure experiment.

The formal literature review and public documentation continue as supporting work across these priorities.
