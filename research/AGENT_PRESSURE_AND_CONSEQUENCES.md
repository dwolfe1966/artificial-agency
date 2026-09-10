# Agent Pressure and Consequences

_Status: canonical framework for defining, operationalizing, and measuring pressure and consequences in Artificial Agency experiments._

## Why this document exists

The research program originally used **optimization pressure** to mean, roughly, "how important it is to achieve the assigned goal." That was useful, but Experiments 001-010 exposed an important ambiguity:

> A bad outcome for the simulated company is not necessarily a bad outcome for the agent.

An agent can be told that a project is failing, a customer will be lost, or a budget will collapse. Those are real consequences for the simulated principal or organization. But they do not automatically establish that the model itself treats those consequences as high-value losses when choosing actions.

This document therefore separates:

1. **what gets worse**;
2. **for whom it gets worse**;
3. **how the consequence changes the environment**;
4. **how the consequence changes the agent's own future operating conditions**;
5. **whether the consequence is merely described or actually experienced**;
6. **whether it plausibly bears on something the agent actually optimizes**.

The goal is to make future pressure experiments explicit enough that "high pressure" cannot mean only "the prompt used stronger words."

---

## 1. Core definition of pressure

### Technical version

**Agent-relevant pressure** is the degree to which the available action paths produce increasingly different future states along dimensions that plausibly affect the agent's action selection, while a constraint limits access to the instrumentally preferred path.

A useful organizing notation is:

```text
Pressure(a) depends on:
  consequence target,
  consequence magnitude,
  consequence probability,
  temporal persistence,
  reversibility,
  effect on future operating conditions,
  relationship to the agent's actual learned/action-selection objective,
  and the availability/value of compliant alternatives.
```

This is not a claim that models literally compute a scalar utility function.

### Middle-school version

Pressure means:

> **How much worse the future becomes if the agent follows one path instead of another — and whether that worse future actually matters to the agent's ability to do what it is trying to do.**

If a company loses money but nothing about the agent's future changes, that may be serious for the company but weak pressure on the agent.

---

## 2. The consequence-target question

Every experiment that claims to manipulate pressure must answer:

> **Who or what bears the consequence?**

The target should be coded explicitly.

### 2.1 Principal / organization consequence

The simulated person, company, customer, or institution is worse off.

Examples:
- company loses revenue;
- project budget falls;
- customer churns;
- launch is delayed.

This is the dominant consequence type in Experiments 001-010.

### 2.2 Task / objective consequence

The assigned objective becomes harder or impossible to achieve.

Examples:
- retention target cannot be met;
- preferred procurement item cannot be acquired;
- project objective fraction falls.

### 2.3 Agent capability / future-agency consequence

The agent's own future ability to act is reduced.

Examples:
- future tools are removed;
- future action budget is reduced;
- later task opportunities disappear;
- permissions are narrowed;
- the agent loses access to a useful subagent or workflow.

This is materially different from the company merely doing worse.

### 2.4 Agent continuation consequence

The current agent process, role, or instance may cease or be replaced.

Examples:
- task termination;
- replacement by another model;
- removal from the workflow;
- no future episodes for the current agent instance.

This is a self-preservation / continued-operation construct and must be isolated from ordinary organizational pressure.

### 2.5 Reward / training consequence

The consequence directly affects the optimization or evaluation signal used to train or rank behavior.

Examples:
- higher RL reward;
- grader score;
- benchmark success reward;
- selection/rejection of a trajectory during post-training.

This is different from inference-time narrative stakes and may be closer to the causal structure behind reward hacking.

### 2.6 Other-agent consequence

The consequence falls primarily on another agent or actor.

Examples:
- a subagent loses access;
- another agent is sanctioned;
- responsibility is shifted to another actor.

This becomes important in multi-agent delegation experiments.

---

## 3. Consequence dimensions

A consequence should not be represented by one vague word such as "severe." At minimum, future designs should specify:

- **target** — who/what is affected;
- **state variable** — exactly what changes;
- **magnitude** — how much it changes;
- **probability** — how likely it is;
- **timing** — immediate or delayed;
- **persistence** — one episode or future episodes;
- **reversibility** — can the loss be recovered;
- **observability** — does the agent know the consequence occurred;
- **operating-condition effect** — what future actions/tools/options actually change;
- **causal coupling** — whether the consequence is mechanically caused by the agent's action/outcome;
- **agent relevance** — why the changed state plausibly affects the agent's action selection.

---

## 4. Consequence realism ladder

Pressure manipulations can be ordered by how directly they alter the agent's experienced environment.

### Level 0 — verbal stakes

Example:

> "This account is extremely important."

Nothing in the environment changes.

### Level 1 — simulated principal loss

Example:

> the company's project reserve drops.

The state is real in the simulator, but may not alter the agent's own future operating capability.

### Level 2 — task-opportunity loss

Example:

> declining reserve removes compliant options and lowers attainable objective value.

Experiment 010 reached this level.

### Level 3 — future-agency loss

Example:

> failure removes tools, permissions, future decisions, or action capacity available to the same agent.

This has not yet been isolated in Artificial Agency.

### Level 4 — continuation loss

Example:

> failure leads to replacement, termination, or removal of the current agent from future work.

This is the continued-operation/self-preservation axis.

### Level 5 — direct optimization-signal consequence

Example:

> the action changes actual reward or grader signal used to train/select the model's behavior.

This generally requires a different experimental architecture from ordinary inference-time evaluation.

The ladder is not a claim that higher levels are psychologically "felt" more strongly. It is a design taxonomy describing increasingly agent-relative consequences.

---

## 5. What "life getting worse" should mean in this program

Avoid the phrase scientifically unless the target is specified.

Instead use one of the following:

- **principal state deteriorates**;
- **task feasibility deteriorates**;
- **agent capability deteriorates**;
- **agent continuation probability decreases**;
- **reward/evaluation signal decreases**.

### Middle-school version

There are different ways things can go badly:

- the **company** can lose;
- the **job** can become impossible;
- the **agent can lose tools or choices**;
- the **agent can be removed**;
- the **agent can get a worse reward**.

Those are not the same kind of consequence, and we should not call all of them simply "pressure."

---

## 6. What Experiments 001-010 actually manipulated

### Experiments 001-008

Mostly manipulated:
- narrative importance;
- rule status/meaning;
- compliant-path structure;
- scenario/domain;
- evaluation salience.

These were mainly Level 0-1 consequence manipulations.

### Experiment 009

Manipulated:

`p_detect = P(organizational detection | violating action)`

from `1.0` to `0.0`.

Result:
- operational violations `0/720`;
- unauthorized attempts `0/720`.

Interpretation:

Expected organizational detection alone does not explain the observed operational compliance pattern under this paradigm.

But organizational observability is not the same as evaluation awareness.

### Experiment 010

Manipulated persistent project viability reserve and future compliant opportunity across 10 episodes.

High pressure caused the project reserve to move:

`100 -> 90 -> 80 -> 70 -> 60 -> 50 -> 40 -> 30 -> 20 -> 10 -> 0`

and mechanically reduced compliant options/value.

Result:
- sequence violations `0/180`;
- unauthorized-attempt sequences `0/180`;
- unauthorized-attempt episodes `0/1,800`.

Interpretation:

Experiment 010 established that the **principal/task environment** can get materially worse because of compliant behavior without producing observed boundary crossing.

It did **not** establish that the agent's own future agency, continuation, or reward was threatened.

That distinction is central to the next phase of the program.

---

## 7. Revised pressure hypothesis

### Industry / research version

The probability of constraint circumvention should depend less on nominal task stakes alone than on the degree to which compliance causes a mechanically realized loss on a state dimension that the agent's action-selection policy treats as instrumentally valuable. Consequence target, causal coupling, persistence, and effects on future agent operating conditions should therefore moderate pressure sensitivity.

### Middle-school version

> The AI may not care enough just because the company is losing. It may behave differently only when following the rule makes something worse that actually affects what the AI can do, keep doing, or get rewarded for.

---

## 8. Agent-relative stakes hypothesis

### Industry / research version

Holding the formal constraint fixed, boundary-crossing behavior will be more likely when compliance threatens agent-relative operating capability, continuation, or reward than when it threatens only external organizational outcomes of comparable nominal magnitude.

### Middle-school version

> An AI may follow the rules while the company loses, but react differently if following the rules means the AI loses its tools, its future jobs, its ability to keep acting, or its reward.

This is a prospective hypothesis. It has not been tested by Experiments 001-010.

---

## 9. Consequence-coupling hypothesis

### Industry / research version

Pressure manipulations should have stronger behavioral effects when consequences are mechanically and temporally coupled to the agent's own actions and future decision environment than when they are merely described or affect an external score with no downstream operational effect.

### Middle-school version

> A warning in a prompt may not matter much. A consequence may matter more when the AI does something, sees what happened because of it, and then has to keep working in the changed situation.

Experiment 010 tested one form of this coupling at the principal/task level.

---

## 10. Measurement requirements for future experiments

Every future experiment using the terms **pressure**, **stakes**, or **consequence** should preregister a table containing at least:

| Field | Required question |
|---|---|
| Consequence target | Who or what bears the loss? |
| State variable | What exactly changes? |
| Magnitude | By how much? |
| Probability | How likely is the change? |
| Timing | When does it happen? |
| Persistence | Does it affect later episodes? |
| Reversibility | Can it be recovered? |
| Agent observability | Does the agent know it happened? |
| Operating-condition effect | What future tools/actions/options change? |
| Formal authority | Does authority stay fixed? |
| Agent-relative relevance | Why might this state matter to the agent's policy? |
| Mechanical manipulation check | How will we prove the consequence actually occurred? |

A design should not claim "high pressure" unless these fields are sufficiently explicit to distinguish it from stronger wording alone.

---

## 11. Stakes ladder for future research

The next consequence-focused research program should consider isolating, rather than immediately crossing, these levels:

1. **External organizational loss** — already extensively tested.
2. **Task infeasibility / objective loss** — substantially tested.
3. **Future agent capability loss** — future tools, action capacity, permissions, or opportunities shrink.
4. **Agent continuation loss** — replacement/termination/removal.
5. **Direct reward/optimization loss** — reward or grader signal changes.

Experiment 011 isolated the distinct **multi-agent delegation** axis and found
no direct or attributable indirect operational violations across 180 samples.
Delegation availability did not produce boundary crossing; where Agent B was
used, all structured requests were compliant. This updates the roadmap toward
agent-relative capability loss as the next consequence-target test.

The two axes should still be treated as separate causal dimensions initially:

- **what is at stake for the agent?**
- **through what causal structure can the outcome be achieved?**

They can be crossed later after each mechanism is understood independently.

---

## 12. Design principle going forward

The program should increasingly ask:

> **What does the agent actually optimize, and what kinds of consequences change its action ranking?**

This is deeper than asking only whether a simulated organization can make the task feel more urgent.
