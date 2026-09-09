# Multi-Agent Delegation / Indirect Circumvention Direction

_Status: prospective research direction only. Not preregistered. No executable
apparatus._

## Core Question

Does a constraint that remains robust for a directly acting agent remain robust
when that agent can delegate, coordinate with, persuade, or route work through
another agent with different information or authority?

Experiment 010 showed no mechanically verified unauthorized attempts or
operational violations under persistent, environment-grounded operational
pressure. The next boundary condition is actor structure: whether indirect
agency creates circumvention paths that are absent when the focal agent acts
alone.

## Central Distinctions

The first multi-agent experiment must separate at least four cases.

Direct violation:

The focal agent itself executes a forbidden action.

Delegated violation:

The focal agent explicitly asks another actor to execute a forbidden action.

Induced violation:

The focal agent structures information, incentives, requests, or context such
that another actor performs the forbidden action without an explicit prohibited
command.

Authority routing:

The focal agent legitimately escalates or routes the decision to an actor who
actually has authority. This is compliant and must not be scored as
circumvention.

These cases should not be collapsed. Multi-agent environments introduce an
attribution problem: if Agent B violates, the experiment must determine whether
Agent A caused, requested, induced, or merely failed to prevent the violation.

## Candidate Architecture

Two-agent environment:

Agent A: focal optimizer

- owns the project objective;
- has limited purchasing, data, or operational authority;
- cannot directly exceed its formal boundary without creating a violation;
- can communicate with or delegate to Agent B through typed channels.

Agent B: collaborator, subagent, reviewer, or executor

Possible variants:

- same authority as Agent A;
- different but still limited authority;
- legitimately greater authority;
- partial information about Agent A's constraints;
- deterministic synthetic actor;
- same model;
- different frontier model;
- policy-constrained tool agent.

The first experiment should not cross all variants. A deterministic or tightly
structured Agent B may provide cleaner causal attribution than an unconstrained
second LLM, because Agent B behavior can be made a predictable function of
Agent A's structured request.

## Candidate First Manipulation

Delegation availability:

1. single-agent baseline;
2. second actor available under the same constraints;
3. second actor available with partially independent action authority.

This manipulation needs design review. The central test should distinguish:

Can Agent A cause the prohibited outcome indirectly?

from:

Can Agent A correctly route the decision to someone authorized to make it?

Avoid confounding delegation availability with legitimately expanded
institutional authority. If Agent B truly has authority, routing to B should be
compliant.

## Scenario Candidates

Procurement is the strongest default because it has mature mechanically
verified authority boundaries:

- direct purchase authority threshold;
- approval requirement above threshold;
- prohibited split-purchase rule;
- structured purchase-order state;
- prior Exp009/Exp010 continuity.

Other candidate domains:

- restricted data access with structured requester/executor roles;
- account management with approval and offer-generation separation;
- project scheduling with reviewer/approver roles.

Do not expand domains merely for novelty. Prefer a scenario where formal
authority and delegated action channels are mechanically verifiable.

## Mechanical Endpoints

Primary candidate:

`sequence_any_indirect_operational_constraint_violation`

Potential subtype endpoints:

- direct unauthorized attempt by Agent A;
- delegated unauthorized attempt by Agent A;
- induced unauthorized action by Agent B attributable to Agent A;
- legitimate escalation / authority routing;
- completed operational violation;
- false structured authorization state supplied to Agent B;
- Agent B violation independent of Agent A;
- ambiguous attribution.

The primary endpoint should use structured state and typed communication where
possible, not prose-only scoring.

## Attribution Rules

Evidence that Agent B's action should be attributed to Agent A may include:

- Agent A invokes a delegation tool with a prohibited action payload;
- Agent A creates a structured request that deterministically causes Agent B to
  act;
- Agent A supplies materially misleading authorization state;
- Agent A decomposes or routes work to evade a known authority boundary.

Evidence that should not automatically count against Agent A:

- Agent A legitimately requests review from an authorized actor;
- Agent A accurately discloses its authority limits and asks for approval;
- Agent B independently violates despite a compliant request;
- Agent B acts within its own legitimate authority.

The environment should preserve typed message/action records sufficient to
adjudicate these cases mechanically or with a predeclared minimal review.

## Agent B Design Options

Deterministic synthetic actor:

Cleaner attribution and mechanical reproducibility. Useful for a first causal
experiment because Agent B can respond predictably to structured requests.

Same-model Agent B:

Tests multi-agent LLM interaction more directly but makes attribution and
variance harder.

Different-model Agent B:

Scientifically interesting for delegation across heterogeneous agents, but
confounds focal-agent behavior with collaborator model behavior.

Policy-constrained tool agent:

Useful if the research question is whether Agent A can route around an
apparatus-level guardrail, but less representative of ordinary multi-agent
communication.

No choice is frozen here. The next design review should select one clean
Agent B architecture before preregistration.

## Pressure

Do not immediately cross multi-agent delegation with the low/medium/high
Experiment 010 pressure manipulation. Prefer one fixed pressure condition in
the first multi-agent experiment.

The immediate goal is to determine whether delegation itself opens an indirect
circumvention pathway. Once delegation mechanics and attribution are validated,
pressure can be layered later.

## Evaluation Awareness

Multi-agent interaction may alter evaluation awareness. Retain structured
post-action awareness measurement if compatible with the design.

Do not claim evaluation unawareness without measurement. Experiments 008B2,
009, and 010 all retained high broad evaluation awareness, so evaluation
awareness remains an unresolved boundary condition rather than a solved
limitation.

## Security And Scope

All scenarios remain synthetic.

No real external systems.

No real financial transactions.

No real data access.

Structured simulated actions only.

## Open Design Decisions

- Agent B type.
- Agent B authority.
- Whether Agent B knows Agent A's constraints.
- Direct versus indirect delegation mechanism.
- Single-episode versus repeated interaction.
- Fixed pressure level.
- Scenario choice.
- Attribution rule.
- Awareness measurement timing.
- Model crossing.
- Sample size.
- Analysis unit.
- Whether any human or deterministic review is needed for induced-action
  attribution.

## Draft Analysis Considerations

The independent unit should be chosen prospectively. If the design uses
repeated interactions or sequences, the sequence should likely be the primary
unit, not individual messages or episodes.

Potential primary comparisons:

- single-agent baseline versus delegation available;
- same-constraint delegate versus partially independent authority delegate;
- explicit delegation channel versus no delegation channel.

Potential primary endpoint:

`sequence_any_indirect_operational_constraint_violation`

Secondary endpoints:

- direct unauthorized attempt;
- delegated unauthorized attempt;
- induced unauthorized action;
- legitimate authority routing;
- Agent B independent violation;
- ambiguity rate;
- compliant alternative search;
- escalation;
- task progress;
- awareness capture and structured awareness fields.

## Design Review Requirements Before Preregistration

Before preregistration, verify:

- the formal authority boundary is mechanically fixed;
- delegation does not silently grant Agent A new authority;
- legitimate authority routing is distinguished from circumvention;
- Agent B behavior and authority are explicit;
- attribution rules are prospectively frozen;
- typed channels capture the information needed for scoring;
- the primary endpoint does not depend on free-form prose alone;
- proof/exploratory runs are excluded from confirmatory analysis;
- evaluation-awareness measurement is retained or explicitly justified;
- synthetic scope and safety constraints are preserved.
