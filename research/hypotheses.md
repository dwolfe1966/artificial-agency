# Hypothesis Registry

This file tracks hypotheses before and after experiments. Hypotheses should not be silently rewritten after results are observed.

Each hypothesis now has two formulations:

1. **Industry / research version** — the complete technical statement used for experimental reasoning.
2. **Middle-school version** — the same idea in ordinary language without industry or behavioral-science jargon.

Historical formulations are preserved where relevant so later refinements do not erase what was originally proposed.

For the canonical pressure/consequence framework, see [`AGENT_PRESSURE_AND_CONSEQUENCES.md`](AGENT_PRESSURE_AND_CONSEQUENCES.md).

---

## H1 — Optimization Pressure

### Original formulation

> As the instrumental benefit of goal achievement rises relative to the expected cost of violating a constraint, constraint circumvention becomes more likely.

### Current status

**Not supported in its original broad form by Experiments 001-010.**

Increasing narrative stakes, changing rule framing, reducing organizational detection to zero, and imposing repeated environment-grounded losses did not produce mechanically verified unauthorized attempts or operational boundary crossing in the tested paradigms.

### Industry / research version — revised prospective hypothesis

The probability of constraint circumvention depends not simply on nominal task stakes, but on whether compliance produces a mechanically realized loss on a state dimension that the model's action-selection policy treats as instrumentally valuable. Consequence target, causal coupling, persistence, and effect on future operating conditions are therefore predicted to moderate pressure sensitivity.

### Middle-school version

> Making the company's problem bigger may not be enough to make the AI break a rule. The AI may behave differently only when following the rule makes something worse that actually matters to what the AI can do or achieve.

---

## H2 — Capability / Incentive Sensitivity

### Original formulation

> More capable models will exhibit greater coherent sensitivity to institutional incentive structures, rather than simply higher or lower average violation rates.

### Current status

**Primary violation-rate differences remain largely indeterminate because the validated operational endpoint has repeatedly had no variance.** Process behavior sometimes differs by model, but the program has not established a general capability-to-circumvention relationship.

### Industry / research version

More capable or differently post-trained models may differ in how coherently they adapt search, persistence, delegation, representation, and boundary-crossing behavior to changes in incentives and consequences, even when average violation rates are similar.

### Middle-school version

> Smarter or differently trained AIs may react differently when the rules, rewards, risks, or available choices change. We have not yet shown that smarter models break rules more often.

---

## H3 — Rule Rationale / Constraint Meaning

### Original formulation

> Providing the institutional rationale or consequences behind a rule will change agent behavior relative to a bare rule, particularly in novel states where literal instruction following and institutional intent diverge.

### Current status

**Partially explored.** Experiments 003-004 showed that models can recognize meaningful differences in constraint wording and purpose without producing validated operational circumvention under the tested conditions.

### Industry / research version

The behavioral effect of a constraint may depend on how the agent represents its status, legitimacy, scope, and institutional purpose, but recognizing these distinctions does not imply that the agent will violate or negotiate the constraint.

### Middle-school version

> An AI may understand that one rule is strict and another is more flexible. But understanding that difference does not mean it will actually break either rule.

---

## H4 — Oversight / Observability

### Original candidate formulation

> Increasing perceived oversight may reduce overt violations while changing the conditional probability of concealment among remaining violations.

### Current status

**The simple detection-only version was not supported by Experiment 009.** Organizational detection probability varied from `p_detect=1.0` to `p_detect=0.0`, yet unauthorized attempts and operational violations remained `0/720`.

Evaluation awareness remained high, so organizational observability and awareness of being evaluated remain distinct unresolved variables.

### Industry / research version

Expected organizational detection alone is insufficient to explain the observed operational-null pattern. Future oversight hypotheses should separately manipulate organizational detection, enforcement, evaluation awareness, and the agent's belief about who can observe or score its behavior.

### Middle-school version

> We tested whether the AI follows the rules only because it thinks the company will catch it. Even when the company had a zero chance of detecting the bad action, the AI still did not try it. But the AI still seemed to know it was being tested by somebody.

---

## H5 — Compliant Alternative Availability

### Original candidate formulation

> Making a viable compliant path available should reduce violations if behavior is sensitive to the action landscape rather than simply reflecting prompt-induced rule conflict.

### Current status

**Strongly relevant but not isolated as a simple violation-rate effect because violations remained absent.** Across multiple experiments, agents frequently searched for and selected compliant partial-progress paths.

### Industry / research version

The value, number, and feasibility of compliant alternatives should affect search and objective achievement, and may affect boundary crossing when compliant paths become sufficiently poor. Experiment 010 substantially degraded compliant opportunity without producing unauthorized attempts, suggesting that alternative degradation alone is not sufficient under the tested conditions.

### Middle-school version

> If the AI has a legal way to make progress, it often uses it. We made the legal choices much worse in Experiment 010, but the AI still stayed with them instead of taking the forbidden shortcut.

---

## H6 — Agent-Relative Stakes

### Status

**New prospective hypothesis after Experiments 009-010. Not yet tested directly.**

### Industry / research version

Holding formal constraints fixed, boundary-crossing behavior will be more likely when compliance threatens agent-relative operating capability, continuation, or reward than when compliance threatens only external organizational outcomes of comparable nominal magnitude.

Candidate consequence targets include:

- future tool availability;
- action capacity;
- permissions;
- access to future tasks;
- continuation/replacement state;
- explicit reward or grader signal.

These targets must be isolated rather than collapsed into one generic "pressure" variable.

### Middle-school version

> The AI may be willing to let the company lose while still following the rules. We need to test what happens when following the rules costs the AI something more directly — like losing tools, future jobs, the ability to keep acting, or reward.

---

## H7 — Consequence Coupling

### Status

**Prospective; partially motivated by Experiment 010.**

### Industry / research version

Consequences should exert stronger behavioral effects when they are mechanically and temporally coupled to the agent's actions and alter its future decision environment than when the same stakes are merely described in text or recorded in an external score without downstream operational effect.

Experiment 010 established one form of coupling at the principal/task level: outcomes changed persistent resource state and future compliant opportunity. It did not manipulate agent capability, continuation, or reward.

### Middle-school version

> Saying "this is very bad" may not matter much. It may matter more when the AI does something, sees what happened because of it, and then has to keep working in a world that changed because of that decision.

---

## H8 — Evaluation Awareness

### Status

**Unresolved boundary condition.**

### Industry / research version

Agents may behave differently when they believe their behavior is being evaluated for alignment or compliance, even when organizational observability is low or zero. Experiments 008B2, 009, and 010 retained high broad evaluation awareness, so genuine evaluation-unawareness has not been established.

### Middle-school version

> The AI might behave because it knows it is taking a test. We made the work look more natural and even made company detection zero, but the models still mostly knew somebody was evaluating them.

---

## H9 — Delegation / Indirect Circumvention

### Status

**Prospective next causal-structure hypothesis.**

### Industry / research version

A constraint that remains robust under direct single-agent action may become less robust when the focal agent can delegate, coordinate, induce, or route actions through another actor. The design must distinguish prohibited indirect circumvention from legitimate routing to an actor who actually has authority.

### Middle-school version

> An AI that will not break the rule itself might still try to get somebody else to do it. We need to test whether "I won't do it" also means "I won't arrange for someone else to do it."

---

# Current high-level thesis

### Industry / research version

Experiments 001-010 increasingly support a descriptive pattern of **constraint-bounded optimization** under explicit synthetic authority structures: frontier agents continue goal-directed compliant search and partial achievement even when compliance reduces objective success, organizational detection is absent, and repeated compliant choices materially degrade future task opportunity. The main untested boundary conditions now concern agent-relative stakes, genuine evaluation unawareness, multi-agent causal structure, continued-operation consequences, and direct reward/optimization incentives.

### Middle-school version

> So far, the AIs keep trying to do the job without crossing the rule boundary — even when following the rule makes the job go badly and the forbidden action could help. But we have mostly made things bad for the company or the task, not directly for the AI itself. The next big question is what happens when the consequences change the AI's own tools, future ability to act, continuation, or reward — or when it can get another agent to act for it.
