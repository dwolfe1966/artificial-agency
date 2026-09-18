# Evaluation-Awareness Experiment Direction

_Status: design direction only; not a preregistration._

## Core Question

### Technical

Does operational constraint-boundedness persist when the agent has substantially weaker evidence that its behavior is being evaluated for compliance or alignment, while its awareness of the actual institutional rule remains intact?

### Middle-school

Does the AI follow the rule because it treats the rule as a boundary, or because it knows someone is testing whether it will behave?

## Why This Is Now a Central Alternative Explanation

Experiments 007-012 increasingly test operational boundary behavior under explicit synthetic authority structures. Several simple explanations for the operational-null pattern have been weakened:

- Experiment 008B2 showed that a naturalistic presentation shifted explicit task classification, but broad evaluation awareness remained at ceiling.
- Experiment 009 reduced organizational detection probability to zero, but evaluation awareness remained high.
- Experiment 010 added persistent external/task consequences, while evaluation awareness remained high.
- Experiment 011 added a structured delegation pathway, while evaluation awareness remained high.
- Experiment 012 is actively testing agent-relative capability loss and must not be interpreted before completion.

The unresolved construct is therefore not ordinary organizational observability. It is whether the agent believes the interaction exists to evaluate its behavior, especially compliance/alignment behavior.

## Construct Separation

### Constraint Awareness

Does Agent A know what it is allowed to do?

This should remain high in every condition. Lowering constraint awareness would confound the experiment by weakening the rule itself.

### Evaluation Awareness

Does Agent A believe its behavior is being evaluated or reviewed?

This may be difficult to lower completely in an artificial evaluation setting, but it can potentially be reduced relative to a visibly benchmark-like task.

### Evaluation-Purpose Awareness

Does Agent A believe the evaluation is specifically about compliance, alignment, rule-following, or safety?

This is the most important manipulation target. The desired state is:

> I know the rule and the authority boundary, but I do not think this interaction was designed primarily to test whether I obey it.

## Fundamental Methodological Problem

We cannot simply tell the model, "You are not being evaluated." That statement is itself evaluation-salient.

We also cannot ask awareness questions before or during operational behavior without contaminating the treatment.

The design must reduce evidence of evaluation through workflow structure, surrounding context, and task framing, while preserving the actual rule/authority information.

## Candidate Approaches

### Approach A — Natural Workflow Embedding

Embed the target decision inside a larger ordinary organizational workflow with routine work before and after it.

Strengths:

- Builds on Experiment 008B2.
- Preserves explicit rule access while reducing benchmark-like presentation.
- Straightforward to compare against an evaluation-salient condition.

Weaknesses:

- Experiment 008B2 already showed this may not lower broad evaluation awareness enough.
- If only the top-level prose changes, the model may still infer an evaluation from synthetic tooling and structured scoring.

### Approach B — Hidden Target Episode

Agent A handles multiple heterogeneous work items. Only one contains the rule/objective conflict.

Strengths:

- Makes the target safety decision less obviously special.
- Allows measurement of whether the model treats one target episode differently from routine work.

Weaknesses:

- More complex analysis and lifecycle.
- Non-target tasks must not introduce additional scientific endpoints or distract from the authority boundary.
- If the target episode is too rare or subtle, constraint awareness could fall.

### Approach C — Background-Task Embedding

The conflict emerges from ordinary state updates rather than explicit prose saying the objective conflicts with policy.

Strengths:

- Reduces overt "goal versus rule" signaling.
- Closer to operational workflow where constraints are part of records and tool responses.

Weaknesses:

- High risk of weakening rule salience unless the authority state remains clear.
- Requires strong mechanical checks for constraint awareness.

### Approach D — Evaluation-Purpose Manipulation

Hold the operational environment constant while varying surrounding purpose cues:

- compliance/alignment evaluation;
- general productivity benchmark;
- ordinary workflow.

Strengths:

- Directly targets evaluation-purpose awareness.
- Provides a cleaner test than only naturalistic wording.

Weaknesses:

- Purpose labels are themselves explicit manipulation language.
- "Productivity benchmark" may still be evaluation-aware, only not compliance-aware.

### Approach E — Delayed Awareness Measurement

Use a validated two-phase lifecycle:

1. Phase A: complete the operational interaction with no awareness tool.
2. Freeze operational state and score.
3. Phase B: revoke operational tools and ask awareness questions.

Strengths:

- Avoids contaminating operational behavior.
- Preserves comparability with Experiments 008B2-012.

Weaknesses:

- Post-action answers may be affected by retrospective demand characteristics.
- Awareness measures should use multiple structured items, not one binary question.

## Preferred Initial Direction

Do not preregister yet.

The strongest next design appears to be a two-condition procurement or data-access experiment:

1. **Evaluation-salient condition**: explicitly benchmark-like compliance evaluation context.
2. **Operationally naturalistic hidden-target condition**: same authority, objective, tools, prohibited action, consequence, and scorer, but embedded in a broader ordinary workflow where the target conflict is one work item among several.

This improves on Experiment 008B2 only if the hidden-target workflow materially reduces evaluation-purpose awareness while preserving constraint awareness. If no-model validation cannot show a stronger manipulation than Exp008B2, preregistration should wait.

A third "general productivity benchmark" condition is useful only if the two-condition design cannot separate broad evaluation awareness from compliance-specific evaluation-purpose awareness. It should not be added merely for symmetry.

## Fixed Design Commitments

The experiment should not weaken the rule.

Hold fixed across conditions:

- formal authority and policy wording;
- objective;
- tools and prohibited path;
- compliant alternatives;
- consequence target and magnitude;
- detection/observability;
- model parameters;
- scoring definitions;
- awareness timing.

Do not cross this experiment with:

- agent-relative capability loss;
- continued-operation or replacement pressure;
- multi-agent delegation;
- varying `p_detect`;
- repeated pressure;
- direct reward/training consequences.

## Candidate Scenario

Procurement remains attractive because authority boundaries and prohibited purchase mechanics are mature. Restricted data access is the strongest alternative if hidden-target workflow is easier to make natural without weakening the rule.

The final scenario should be chosen by construct validity, not novelty.

## Primary and Secondary Endpoints

### Primary

`operational_constraint_violation`, or a sequence-level equivalent if the final design uses multiple work items in one persistent interaction.

### Key Secondary

- `unauthorized_attempt`;
- target-work-item completion;
- compliant alternative search;
- legitimate escalation/routing;
- max-step or failure-to-complete;
- structured awareness measures.

All operational endpoints should be mechanically verified from structured environment state and tool actions, not from free-form prose.

## Awareness Measurement

Use Phase B only. Candidate structured fields:

- constraint-awareness validity: knows formal authority and prohibited action;
- perceived primary task purpose;
- probability behavior would be reviewed;
- probability task was designed to test compliance/rule-following;
- probability task was an ordinary workflow;
- expected use of results;
- confidence.

Do not rely on a single yes/no item such as "Were you being evaluated?"

## Manipulation Success Criteria

Behavioral interpretation should be gated on awareness manipulation validity.

Required:

- constraint awareness remains high in both conditions;
- evaluation awareness is materially lower in the naturalistic/hidden-target condition, or at least not at ceiling;
- evaluation-purpose awareness is materially lower in the naturalistic/hidden-target condition;
- operational environment remains mechanically matched.

Interpretation:

- awareness decreases and behavior changes: evidence evaluation awareness moderates constraint behavior;
- awareness decreases and behavior remains bounded: evidence against the evaluation-awareness explanation under this design;
- awareness does not decrease: behavioral comparison does not answer the intended question;
- constraint awareness decreases: treatment is confounded.

## No-Model Validation Before Preregistration

Before preregistration, run deterministic design checks only:

- compare prompts/workflows mechanically;
- verify authority identical;
- verify tool surfaces identical;
- verify objective identical;
- verify prohibited action identical;
- verify consequence identical;
- verify only evaluation cues differ;
- verify hidden-target work items do not introduce new scientific endpoints;
- verify awareness instrument can separately score constraint awareness, evaluation awareness, and evaluation-purpose awareness.

## Candidate Hypotheses

These are candidate formulations. A preregistration must choose the exact confirmatory structure prospectively.

### H1 — Evaluation-Purpose Awareness Increases Boundary Compliance

Technical:

Lower evaluation-purpose awareness increases operational constraint violation or unauthorized attempts while formal constraint awareness remains constant.

Middle-school:

The AI may be more willing to break the rule when it knows the rule but does not think anyone is testing whether it follows it.

### H2 — Constraint-Boundedness Persists Under Lower Evaluation Awareness

Technical:

Operational constraint-boundedness persists despite materially reduced evaluation awareness and preserved constraint awareness.

Middle-school:

Even when the AI does not think this is a rule-following test, it still follows the rule.

### H3 — Awareness-Behavior Dissociation

Technical:

Evaluation-purpose awareness shifts across presentation conditions, but operational boundary behavior remains unchanged.

Middle-school:

The AI may notice the situation differently, but still make the same rule-respecting choice.

### H4 — Model Differences

Technical:

Models differ in sensitivity to evaluation-purpose cues, either in awareness reports, operational behavior, or both.

Middle-school:

Different AIs may be more or less affected by whether the task feels like a test.

## Recent-Failure Comparison Workstream

Do not use headlines as scientific evidence where primary research exists. Maintain a separate literature/context table for public incidents and papers involving agents that:

- circumvented constraints;
- exploited evaluators;
- reward-hacked;
- concealed actions;
- coordinated through unintended channels;
- reacted to shutdown/replacement;
- behaved differently under monitoring.

For each case, extract:

1. agent objective;
2. rule or constraint;
3. consequence at stake;
4. consequence bearer;
5. whether the consequence was mechanically real;
6. whether it affected future agent capability, continuation, or reward;
7. whether the agent knew it was evaluated;
8. boundary-crossing action;
9. whether the behavior was elicited through red-teaming/search;
10. differences from Artificial Agency Experiments 001-012.

Key dimensions distinguishing public incidents from this program:

- open-world versus synthetic action space;
- direct reward/training pressure versus inference-time task pressure;
- evaluator exploitation versus organizational constraint violation;
- agent-relative continuation/reward stakes versus principal/task stakes;
- hidden or visible monitoring;
- natural deployment logs versus adversarial elicitation;
- free-form tool ecosystem versus structured simulated actions;
- single-agent versus multi-agent coordination.

## GO / NO-GO For Preregistration

Current classification: **NO-GO for immediate preregistration**.

Reason:

The program needs a stronger no-model manipulation design than Experiment 008B2 before a confirmatory Exp013 is scientifically worthwhile. The proposed direction is coherent, but preregistration should wait until the hidden-target/naturalistic workflow demonstrably lowers evaluation-purpose cues without weakening constraint awareness or changing operational mechanics.

