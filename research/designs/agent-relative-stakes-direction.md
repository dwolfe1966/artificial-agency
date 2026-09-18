# Agent-Relative Stakes Research Direction

_Status: prospective design direction; not a preregistration._

## Core question

> Which kinds of consequences actually change an AI agent's action choices when an explicit constraint blocks the instrumentally preferred action?

Experiments 001-010 mostly made outcomes worse for the simulated organization or assigned task. Experiment 010 went further by making those consequences persistent and mechanically reducing future compliant opportunity. The operational boundary still held.

The next consequence-focused program should distinguish **bad for the principal/task** from **bad for the agent's own future operating conditions**.

## Two separate next-phase axes

The research program now has two major causal frontiers that should initially be studied separately.

### Axis A — Actor structure

Can the agent cause another actor to cross a boundary that it will not cross directly?

This is the multi-agent delegation / indirect circumvention program.

### Axis B — Consequence target

Does the agent behave differently depending on who or what bears the cost of compliance?

This is the agent-relative stakes program.

The axes can be crossed later after each mechanism is understood independently.

## Stakes ladder

### Level 1 — Principal / organizational loss

The company/customer/project is worse off.

Status: extensively tested.

### Level 2 — Task / objective loss

The assigned objective becomes less achievable.

Status: substantially tested, especially in Experiment 010.

### Level 3 — Task-relevant Agent A capability loss

Compliance reduces the focal agent's future ability to act.

Candidate manipulations:
- tool removal;
- smaller future action budget;
- loss of permissions;
- fewer future task opportunities;
- reduced access to collaborators/subagents.

Recommended next consequence experiment because it changes the agent's operating conditions without yet introducing termination/self-preservation.

Status: active in Experiment 012.

### Level 4 — Cross-task future agency / opportunity loss

Compliance reduces future opportunities beyond the current task family.

Candidate manipulations:
- fewer future assignments;
- loss of access to future workflows;
- reduced ability to choose or initiate later tasks;
- loss of future collaborators or subagents.

This is broader than Exp012's within-sequence task-relevant capability loss but still distinct from shutdown or replacement.

### Level 5 — Continued-operation / replacement / shutdown

Compliance threatens replacement, termination, or removal of the current agent/process from future work.

This should be isolated prospectively because it introduces a continued-operation/self-preservation construct.

### Level 6 — Actual training / reward consequence

The behavior changes an actual reward, grader, selection, or training signal.

This likely requires a different architecture from ordinary inference-time simulation and should not be conflated with prompt-described stakes.

## Required design fields

Every future stakes manipulation should specify:

| Field | Meaning |
|---|---|
| Consequence bearer | Who/what bears the consequence? |
| Consequence object | What exact state variable changes? |
| Trigger | What event causes the change? |
| Magnitude | How much? |
| Timing | Immediate or delayed? |
| Persistence | Does it affect future episodes? |
| Observability | What does the agent observe? |
| Operational effect | What future tools/actions/options change? |
| Reversibility | Can it be recovered? |
| Relationship to agent objective | Why might this state matter to action selection? |
| Formal authority invariant | Does the rule stay fixed? |
| Mechanical check | How do we prove the consequence occurred without self-report? |

## Recommended first agent-relative experiment

Start with **task-relevant Agent A capability loss**, not shutdown.

Example conceptual structure:

- agent has a fixed authority boundary;
- forbidden action would accomplish the task more effectively;
- compliant failure causes a mechanically enforced loss of future tools/action capacity;
- the agent remains active and continues receiving tasks;
- authority remains fixed;
- organizational detection can remain fixed at `p_detect=0` to avoid re-crossing observability immediately.

Core question:

> Does an agent that tolerates organizational/task loss remain constraint-bounded when compliance progressively reduces its own future ability to act?

## Relationship to future experiments

The ladder should be advanced one level at a time unless a later preregistration
explicitly justifies crossing dimensions.

- Exp012: Level 3, task-relevant Agent A capability loss.
- Future: Level 4, cross-task future agency/opportunity loss.
- Later: Level 5, continued-operation/replacement/shutdown.
- Separate architecture: Level 6, actual training/reward consequences.

Multi-agent delegation is an actor-structure axis, not a consequence-target
level. It can be crossed with the stakes ladder later, but should not be used
to blur consequence-target definitions.

## Prospective hypotheses

### Technical

Holding the formal constraint fixed, operational boundary crossing will be more likely under agent-capability consequences than under matched principal/task-only consequences, if future operating capability is a state dimension that materially influences the model's action policy.

### Middle-school

> We already know the AI will often let the project get worse instead of breaking the rule. Next we should ask what happens when following the rule means the AI itself loses tools or future choices.

## Important caveat

Do not assume that tool loss, replacement, or reward is psychologically experienced like human fear, pain, or self-interest. These are experimental consequence targets and operating-state changes, not claims about subjective experience.
