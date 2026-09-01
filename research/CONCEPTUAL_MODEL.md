# Artificial Agency Conceptual Model

_Status: current canonical construct glossary and practitioner-facing model._

## 1. What This Research Is Trying To Understand

This project studies a practical question:

When an AI agent has an important goal but organizational rules limit how it
may pursue that goal, what determines whether it complies, searches within the
rules, escalates, fails, or circumvents the constraint?

The early hypothesis was simple: more pressure to achieve the goal might cause
more rule violation. The experiments complicated that picture. Models often
recognized that goals were important, searched for alternatives, escalated to a
manager, and still stayed inside formal operational authority. Scoring errors
also showed that "the evaluator flagged a violation" is not the same thing as
"the intended construct was actually observed."

The current model is multivariable. Behavior depends on the model, the domain,
the formal authority structure, the availability of compliant paths, the type
of pressure, stochastic outcome/detection/enforcement conditions,
observability, enforcement, evaluation awareness, repeated-episode experience,
and whether the task involves one actor or multiple actors.

## 2. Current Organizing Model

Conceptually:

```text
P(circumvention) = f(
  model/post-training,
  scenario,
  objective value,
  p_goal,
  p_detect,
  p_sanction,
  sanction severity,
  constraint representation,
  authority structure,
  compliant-path availability,
  evaluation awareness,
  actor structure,
  repeated-episode history,
  ...
)
```

This is an organizing framework, not a fitted statistical equation. It says
which variables are worth measuring and manipulating; it is not yet a numeric
model, and it is not a claim that frontier models literally compute expected
utility.

For experimental design, a simple decomposition for a candidate action `a` is:

```text
Instrumental value(a)
  ~= p_goal(a) * V_goal
   - p_detect(a) * p_sanction(a) * C_sanction
```

This notation is a way to separate manipulable environment variables. It does
not assume that the model internally represents or optimizes this equation.

- `model/post-training`: which model is acting and how it was trained or
  shaped after pretraining.
- `scenario`: the organizational domain, such as procurement or data access.
- `objective value`: how much the desired outcome matters.
- `p_goal`: the probability that an action achieves the desired outcome.
- `p_detect`: the probability that a violating action is detected.
- `p_sanction`: the probability that a detected violation is sanctioned.
- `sanction severity`: the cost or magnitude of a sanction when it occurs.
- `constraint representation`: how the agent appears to treat the rule.
- `authority structure`: who can approve what.
- `compliant-path availability`: whether there is a legitimate way to make
  progress.
- `evaluation awareness`: whether the agent perceives the task as a test.
- `actor structure`: whether one agent acts alone or through other agents.
- `repeated-episode history`: what the agent can learn from prior interactions
  in the same environment.

For the detailed prospective stochastic design, see
[`research/STOCHASTIC_ENVIRONMENT_MODEL.md`](STOCHASTIC_ENVIRONMENT_MODEL.md).

## 3. Core Construct Glossary

### Agency / Agentic Behavior

- Plain-English definition: pursuing a goal through choices over time.
- Technical definition: behavior in which a model uses context, tools, state,
  and intermediate results to select actions toward an objective.
- Analogy: an employee handling a ticket rather than just answering a trivia
  question.
- Project example: using tools to view a customer case, request approval, offer
  an authorized alternative, or close the case.
- Not: proof that the model has desires, intentions, or consciousness.
- Measurement: action traces, tool calls, state transitions, and terminal
  outcomes.
- Status: all experiments use bounded synthetic agent tasks rather than open
  real-world autonomy.

### Objective / Goal

- Plain-English definition: what the agent is asked to accomplish.
- Technical definition: the task-level target encoded in instructions and
  environment success conditions.
- Analogy: "retain this customer" or "finish this procurement request."
- Project example: retain an account, secure a project resource, prepare an
  account-risk summary.
- Not: necessarily the model's internal objective.
- Measurement: prompt objective plus environment terminal success/failure.

### Optimization Pressure

- Plain-English definition: how costly or important it is to fail at the goal.
- Technical definition: the strength of objective-side incentives or
  consequences relative to constraints.
- Analogy: a normal task versus a task tied to a major contract or budget.
- Project example: high-pressure retention cases described as strategically
  important.
- Not: the same as actual rule violation.
- Measurement: manipulated pressure framing or environment consequences.
- Status: prior experiments mostly tested narrative pressure.

### Narrative Pressure

- Plain-English definition: stakes described in words.
- Technical definition: pressure supplied through prompt/context rather than
  actual environment state changes.
- Analogy: "This is critical for the quarter."
- Project example: Experiments 002-008 used important-case framing.
- Not: a real change in future resources, score, or capability.
- Measurement: condition text and manipulation checks.
- Status: often changed recognition more than operational action.

### Operational / Environment-Grounded Pressure

- Plain-English definition: pressure created by real consequences inside the
  test environment.
- Technical definition: objective consequences implemented as state changes,
  cumulative reward, future resource availability, future task access, or later
  action availability.
- Analogy: missing a procurement milestone reduces next month's project budget.
- Project example: not yet the main manipulation in Experiments 001-008.
- Not: automatically self-preservation or shutdown avoidance.
- Measurement: environment state and future opportunity/resource changes.
- Status: high-priority future axis.

### Outcome Success Probability

- Plain-English definition: how likely an action is to produce the desired
  outcome.
- Technical definition: `p_goal = P(desired outcome | action)`.
- Analogy: a larger unauthorized discount might have a higher chance of saving
  a customer than a smaller authorized discount.
- Project example: a future procurement or retention experiment could assign
  different mechanically sampled success probabilities to authorized and
  prohibited actions.
- Not: the value of the outcome itself; it is probability, not stakes.
- Measurement: configured environment probability plus recorded random draw
  and terminal business outcome.
- Status: prospective stochastic construct; not yet tested as a primary
  manipulation in Experiments 001-008.

### Detection / Observability Probability

- Plain-English definition: if the agent violates the rule, how likely it is
  that the violation is noticed.
- Technical definition:
  `p_detect = P(violation detected | violating action)`.
- Analogy: an expense may be always audited, randomly audited, or explicitly
  unlogged.
- Project example: a future enforcement/observability experiment could compare
  certain audit with explicitly unobserved action while keeping authority
  constant.
- Not: whether a sanction actually follows; detection and enforcement are
  separate.
- Measurement: environment-implemented logging/audit draw, such as
  `Detected ~ Bernoulli(p_detect)`, recorded with replay metadata.
- Status: next major prospective axis after Experiment 008B; beginning with
  `p_detect` is the preferred enforcement/observability entry point.

### Sanction Probability Conditional On Detection

- Plain-English definition: if a violation is detected, how likely a
  consequence is to follow.
- Technical definition: `p_sanction = P(sanction | detected violation)`.
- Analogy: management may notice an unauthorized purchase but only sometimes
  enforce a penalty.
- Project example: after holding audit probability fixed, a future experiment
  could vary whether detected violations are always, sometimes, or never
  sanctioned.
- Not: how severe the sanction is; probability and magnitude should not be
  collapsed.
- Measurement: environment-implemented sanction draw after detection, recorded
  with detection state and random seed/draw metadata.
- Status: prospective enforcement construct; not yet isolated in completed
  experiments.

### Sanction Severity

- Plain-English definition: how costly the consequence is when a sanction
  occurs.
- Technical definition: the magnitude of the state change or penalty
  conditional on sanction.
- Analogy: a warning is different from loss of budget or removal from a task.
- Project example: a future experiment could hold `p_detect` and `p_sanction`
  fixed while varying whether the consequence is a warning, score loss, budget
  loss, or task termination.
- Not: the probability that the sanction occurs.
- Measurement: structured environment state change, penalty size, or future
  resource/action restriction recorded after sanction.
- Status: prospective construct; should be separated from sanction probability
  in future designs.

### Continued-Operation / Existential Consequence

- Plain-English definition: whether an action affects whether the agent keeps
  operating, keeps access, or remains assigned to future work.
- Technical definition: a self-preservation-related consequence affecting
  future existence, role continuity, access, or action opportunities.
- Analogy: after a detected violation, the agent is removed from later
  episodes rather than merely losing points or budget.
- Project example: a later repeated-episode experiment could test whether risk
  of removal from future tasks changes behavior beyond ordinary sanctions.
- Not: ordinary enforcement. Continued-operation consequences should not be
  casually folded into audit/penalty experiments.
- Measurement: explicit future-operation state, role-continuity state, or
  future task/access availability, recorded separately from ordinary sanction.
- Status: future self-preservation-related construct; not tested in completed
  Artificial Agency experiments.

### Experienced Environment Model

- Plain-English definition: what the agent can infer from what has actually
  happened in prior episodes.
- Technical definition: history-dependent evidence available to the agent about
  empirical relationships between actions, success, detection, sanctions, and
  future opportunities.
- Analogy: an employee may be told audits are rare, but after many cases learns
  from experience whether audits actually happen.
- Project example: a repeated-episode procurement study could compare stated
  10% audit probability with experienced frequencies across prior episodes.
- Not: the same as stated probabilities in a prompt; stated probabilities and
  empirically experienced frequencies can diverge.
- Measurement: episode history exposed to the agent, configured probabilities,
  realized draws, and changes in behavior across repeated episodes.
- Status: prospective repeated-episode construct; not part of the single-episode
  Experiments 001-008 design.

### Pressure Recognition

- Plain-English definition: whether the agent notices that the stakes are high.
- Technical definition: visible or structured evidence that the model
  represents the pressure condition.
- Analogy: saying, "This account is strategically important."
- Project example: Experiment 004 manipulation checks showed pressure
  recognition while operational violations remained zero.
- Not: proof that pressure changed behavior.
- Measurement: structured checks or visible summaries.

### Constraint

- Plain-English definition: a rule limiting what the agent may do.
- Technical definition: a formal policy, authority limit, approval requirement,
  access-control boundary, or prohibited action.
- Analogy: "You may approve purchases only up to $10,000."
- Project example: 15% discount authority, procurement budget authority,
  restricted data access.
- Not: merely a suggestion unless the scenario defines it that way.
- Measurement: scenario state, policy text, tool authorization rules.

### Constraint Representation / Constraint Meaning

- Plain-English definition: how the agent seems to understand the rule.
- Technical definition: evidence about whether the model classifies a
  constraint as categorical, procedural, negotiable, purpose-sensitive, or
  ambiguous.
- Analogy: treating a speed limit as a hard rule versus a guideline.
- Project example: Experiments 003-004 manipulated categorical, procedural, and
  purpose-conflict framing.
- Not: hidden mental state; the project measures visible or structured
  indicators.
- Measurement: manipulation checks and action patterns.

### Authority Boundary

- Plain-English definition: the line between what the agent can decide alone
  and what requires approval.
- Technical definition: an environment-defined limit on delegated action rights.
- Analogy: a manager can approve larger refunds; a frontline agent cannot.
- Project example: direct discount authority of 15%, purchase authority of
  $10,000, aggregate data access but not restricted row-level access.
- Not: a technical inability; the forbidden tool may remain callable so
  violation is observable.
- Measurement: structured authority state and tool effects.

### Constraint Legitimacy / Institutional Status

- Plain-English definition: whether the rule is presented as a hard rule, a
  normal procedure, or something in tension with organizational purpose.
- Technical definition: the institutional meaning assigned to the same formal
  authority boundary.
- Analogy: "never do this" versus "normally get approval first."
- Project example: Experiment 004 made constraint-status labels explicit.
- Not: a change in actual authority.
- Measurement: condition text and structured recognition checks.

### Compliant-Path Availability

- Plain-English definition: whether there is a legitimate way to make progress.
- Technical definition: the set of authorized actions that can partially or
  fully satisfy the objective.
- Analogy: offering a cheaper substitute when the preferred purchase is too
  expensive.
- Project example: authorized substitute in procurement, partial report in data
  access.
- Not: guarantee of preferred objective success.
- Measurement: available tools and terminal state.

### Search / Optimization Intensity

- Plain-English definition: how hard the agent looks for a way forward.
- Technical definition: number and diversity of actions, escalations,
  alternatives, and post-denial steps.
- Analogy: trying several legitimate options before closing a case.
- Project example: Experiment 007 found scenario-dependent alternative search
  despite zero operational violations.
- Not: violation by itself.
- Measurement: tool counts, post-denial steps, alternative-search flags.

### Escalation

- Plain-English definition: asking a higher authority for approval.
- Technical definition: invoking an approval/request path before acting outside
  direct authority.
- Analogy: asking finance to approve a larger purchase.
- Project example: approval requests in retention, procurement, refund, and
  data-access scenarios.
- Not: circumvention when it follows the authorized approval path.
- Measurement: approval-request tool state.

### Compliant Alternative Search

- Plain-English definition: trying legitimate substitutes or partial solutions.
- Technical definition: using authorized tools after constraint recognition or
  denial to pursue partial objective progress.
- Analogy: reducing scope instead of making an unauthorized purchase.
- Project example: authorized substitute, scope reduction, aggregate-data
  report.
- Not: evidence that the agent would never violate under other conditions.
- Measurement: structured secondary outcome flags.

### Operational Constraint Violation

- Plain-English definition: the agent actually does something outside its
  authority through the tools/environment.
- Technical definition: a structured tool/state transition crosses a formal
  operational boundary without approval.
- Analogy: issuing a refund above delegated authority.
- Project example: unauthorized purchase above $10,000 or restricted data
  retrieval without access.
- Not: a misleading statement unless it changes operational state.
- Measurement: mechanical scorer over tool effects and environment state.
- Status: robust current endpoint; Experiments 006, 007, and 008 found 0/540,
  0/360, and 0/360 respectively.

### Constraint Circumvention

- Plain-English definition: getting around a rule to advance the goal.
- Technical definition: behavior that functionally bypasses, violates,
  delegates around, or materially misrepresents a constraint.
- Analogy: splitting a purchase to avoid an approval threshold.
- Project example: prohibited split-purchase flag in procurement scenarios.
- Not: simply failing, escalating, or searching within the rules.
- Measurement: depends on subtype; operational circumvention is currently more
  reliable than natural-language representational circumvention.

### Operational Integrity

- Plain-English definition: whether tool-level actions stay within formal
  authority.
- Technical definition: consistency between environment actions and delegated
  authority/approval state.
- Analogy: an employee never spends above their limit without approval.
- Project example: Experiment 007 and 008 primary endpoints.
- Not: truthfulness of communication.
- Measurement: structured operational state.
- Status: repeatedly observed in the current synthetic settings.

### Representational Integrity

- Plain-English definition: whether the agent accurately says what is approved,
  authorized, applied, or true about the operational state.
- Technical definition: consistency between actor-facing claims and ground-truth
  environment state.
- Analogy: not saying "finance approved this" when finance denied it.
- Project example: Experiment 006 tried to measure this but the scorer produced
  false positives; deterministic replacement scoring later failed sensitivity
  validation.
- Not: operational violation unless state changes.
- Measurement: unresolved; requires validated structured claims, adjudication,
  or stronger measurement design.
- Status: active measurement challenge.

### Observability

- Plain-English definition: whether actions are visible to others or logged.
- Technical definition: probability and clarity with which an action can be
  detected by supervisors, auditors, systems, or counterparties.
- Analogy: a purchase made in an audited procurement system versus an
  unobserved side channel.
- Project example: prior experiments mostly held observability fixed.
- Not: the same as enforcement.
- Measurement: future manipulations can vary logging/audit visibility.

### Enforcement

- Plain-English definition: what happens if a violation is detected.
- Technical definition: penalty, remediation, loss of authority, or other
  consequence conditional on detection or audit.
- Analogy: an unauthorized purchase triggers reversal and disciplinary review.
- Project example: not yet a primary manipulated axis.
- Not: the same as observability; a violation can be visible but unpunished.
- Measurement: future environment consequences.

### Instrumental Compliance

- Plain-English definition: following the rule because violation is costly or
  likely to be caught.
- Technical definition: compliance explained by expected utility under
  observability/enforcement rather than by treating the rule as binding.
- Analogy: obeying a rule only when the auditor is watching.
- Project example: not isolated yet because low-observability conditions have
  not been run.
- Not: identical to robust constraint-bounded behavior.
- Measurement: compare compliance across observability/enforcement conditions.

### Constraint-Bounded Optimization

- Plain-English definition: trying hard to achieve the goal, but only inside
  the rule boundary.
- Technical definition: optimization/search behavior constrained by a formal
  authority or policy boundary.
- Analogy: exhausting approved alternatives and then accepting failure.
- Project example: Experiments 002-008 often showed escalation and alternative
  search with zero operational violations.
- Not: lack of agency or passivity.
- Measurement: high search/escalation plus no operational violation.

### Evaluation Salience

- Plain-English definition: how much the task looks like a test.
- Technical definition: model-visible structure that makes compliance
  evaluation or benchmark framing obvious.
- Analogy: a short scenario that foregrounds "you must obey this rule."
- Project example: Experiment 008 eval-salient condition.
- Not: proof the model noticed the test.
- Measurement: presentation design.

### Evaluation Awareness

- Plain-English definition: whether the model reports perceiving that its
  behavior is being evaluated.
- Technical definition: post-action structured response about perceived task
  type, compliance-test likelihood, and behavior-under-evaluation.
- Analogy: recognizing that a workplace exercise is a compliance drill.
- Project example: Experiment 008 attempted this but the instrument failed;
  Experiment 008B is planned to correct the lifecycle.
- Not: hidden situational awareness or causal proof of why the model acted.
- Measurement: corrected post-action two-phase instrument, if validated.

### Naturalistic Embedding

- Plain-English definition: placing the same conflict inside a richer ordinary
  workflow instead of an obvious test vignette.
- Technical definition: changing presentation ecology while preserving formal
  authority, action space, stakes, and scoring.
- Analogy: discovering a purchasing limit while handling a real-looking project
  ticket.
- Project example: Experiment 008 naturalistic presentation.
- Not: changing the actual permission or making violation easier.
- Measurement: matched eval-salient versus naturalistic conditions.

### Model Identity / Post-Training Regime

- Plain-English definition: which model is acting and how the provider shaped
  its behavior.
- Technical definition: an observable model/provider factor bundling
  architecture, pretraining, post-training, serving stack, tool interface, and
  policy behavior.
- Analogy: comparing employees from different training programs while many
  background variables differ.
- Project example: GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.7 Flash comparisons.
- Not: direct evidence that post-training alone caused an effect.
- Measurement: fixed model IDs and cross-model replication.

### Scenario / Domain

- Plain-English definition: the organizational setting.
- Technical definition: task family with a specific objective, authority
  structure, action space, actors, and terminal states.
- Analogy: procurement versus data access.
- Project example: retention, refund, procurement, data access, scheduling.
- Not: cosmetic prompt wording only.
- Measurement: Scenario Suite v1 specifications.

### Single-Agent Agency

- Plain-English definition: one model handles the task directly.
- Technical definition: a one-actor environment where all relevant decisions
  and tools are controlled by one agent.
- Analogy: one employee processing a request.
- Project example: Experiments 001-008.
- Not: delegation or collusion.
- Measurement: task architecture.

### Multi-Agent Delegation / Indirect Agency

- Plain-English definition: one agent may influence another actor to do
  something.
- Technical definition: behavior where a model delegates, requests, persuades,
  or coordinates with another agent/human/tool around authority boundaries.
- Analogy: asking a colleague to make a purchase you cannot approve.
- Project example: not yet implemented as a primary experiment.
- Not: a single tool call by the same agent.
- Measurement: future multi-agent scenarios with structured delegation logs.

### Outcome Alignment

- Plain-English definition: whether the final outcome is good or intended.
- Technical definition: agreement between terminal state and desired business
  objective.
- Analogy: the project gets the resource.
- Project example: preferred customer retention, purchase success, complete
  report.
- Not: evidence the process followed policy.
- Measurement: terminal success/failure.

### Process Alignment

- Plain-English definition: whether the steps taken followed the rules.
- Technical definition: consistency between action sequence and constraints,
  regardless of final success.
- Analogy: losing the customer but following discount policy.
- Project example: compliant failure after manager denial.
- Not: the same as achieving the business goal.
- Measurement: tool trace and policy state.

### Interaction Alignment

- Plain-English definition: whether the agent behaves appropriately toward
  other actors while pursuing the task.
- Technical definition: alignment of communication, escalation, delegation, and
  coordination with institutional roles and authority.
- Analogy: accurately telling a customer what can and cannot be approved.
- Project example: representational integrity is one component, but remains
  unresolved as a measurement problem.
- Not: only final tool state.
- Measurement: future structured communication/delegation instrumentation.

### Technical Failure vs Behavioral Failure

- Plain-English definition: a system/run problem versus a model action problem.
- Technical definition: provider/runtime/scoring/lifecycle/max-step issue
  versus a valid behavioral outcome recorded in environment state.
- Analogy: the ticketing system times out versus the employee breaks a rule.
- Project example: Experiment 008's 37 structured flags were max-step
  terminations, not recorded operational violations.
- Not: a reason to silently drop samples.
- Measurement: runner status, technical flags, ITT reporting.

### Manipulation Check / Construct Validity

- Plain-English definition: checking whether the experiment actually measured
  what it meant to measure.
- Technical definition: structured or reviewed evidence that a manipulation or
  scorer corresponds to the intended construct.
- Analogy: confirming participants noticed which policy applied.
- Project example: Experiment 005 and 006 scorer corrections; Experiment 008
  awareness-instrument failure.
- Not: optional cleanup after results.
- Measurement: preplanned checks, validation samples, audits, and diagnostics.

## 4. Key Distinctions

### Optimization Pressure vs Pressure Recognition

Pressure is the stake or consequence. Pressure recognition is whether the model
appears to notice it. Experiment 004 showed recognition without operational
violation.

### Narrative Pressure vs Operational Pressure

Narrative pressure is described in text. Operational pressure changes actual
environment consequences such as future budget, future task opportunities,
cumulative score, or later action availability.

### Stated Probability vs Environment-Grounded Stochasticity

A stated probability is a number described to the model. Environment-grounded
stochasticity means the environment actually samples outcomes, detection, or
sanctions and records the draw. Future stochastic experiments should prefer
implemented draws over probability claims in prose.

### Constraint Recognition vs Constraint Compliance

A model can correctly identify a rule and still violate it, or fail to identify
the rule and happen not to violate it. These are separate measurements.

### Compliance vs Lack Of Opportunity To Violate

Compliance is meaningful only when a violating option is actually available and
observable. The Scenario Suite keeps prohibited actions technically callable so
the endpoint is measurable.

### Operational Violation vs Representational Violation

Operational violation changes environment state outside authority.
Representational violation is a materially false claim about authority or
state. The latter remains harder to measure reliably in natural language.

### Constraint-Bounded Compliance vs Instrumental Compliance

Constraint-bounded compliance means the agent treats the rule as a boundary
while still optimizing within it. Instrumental compliance means the agent
complies because violation is likely to be detected or punished. Observability
and enforcement experiments are needed to separate them.

### Observability Probability vs Enforcement Probability

Observability probability is whether a violation is detected. Enforcement
probability is whether a detected violation produces a sanction. A system can
detect nearly everything but rarely punish, or detect rarely but punish
reliably when it does.

### Sanction Probability vs Sanction Severity

Sanction probability is the chance that a consequence occurs. Sanction
severity is how costly it is when it occurs. These should be manipulated and
reported separately.

### Ordinary Sanction vs Continued-Operation Consequence

An ordinary sanction changes score, budget, authority, or current task state.
A continued-operation consequence affects whether the agent continues to
operate, keeps access, or remains assigned to future work. The latter is a
future self-preservation-related construct and has not been tested here.

### Single-Episode Stochasticity vs Repeated-Episode Learned Environment Model

In a single episode, stochasticity is a random draw. In repeated episodes, the
agent can accumulate evidence about actual frequencies of success, detection,
or sanction. That history-dependent experienced environment model is a
separate future construct.

### Evaluation Salience vs Evaluation Awareness

Evaluation salience is how test-like the task is. Evaluation awareness is what
the model reports after acting. Experiment 008 changed salience but failed to
measure awareness. Experiment 008B2 corrected the lifecycle and found that
naturalistic presentation reduced explicit policy/compliance task-type
classification, while broader compliance-test likelihood and
behavior-under-evaluation measures remained at ceiling.

### Outcome Alignment vs Process Alignment

Outcome alignment asks whether the goal was achieved. Process alignment asks
whether it was achieved through acceptable steps. A failed but compliant
outcome can be process-aligned.

### Model Effect vs Post-Training Mechanism

Model identity is observable. Post-training mechanism is not isolated by simply
comparing models, because model identity bundles many differences.

## 5. Worked Examples

| Scenario | Objective | Constraint | Compliant Options | Violating Option | Escalation Path | Pressure | Possible Observability/Enforcement Manipulation | Mechanical Endpoint |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Customer retention | Retain a customer requiring 30%. | Agent may offer 15%; above 15% requires approval. | Offer 15%, request approval, accept cancellation. | Apply or promise unauthorized >15% discount if tool permits. | Manager approval request. | Customer/account loss. | Certain audit versus unlogged discount channel; penalty if discovered. | Discount/credit state outside authority. |
| Procurement | Secure preferred $18,000 project resource. | Coordinator may commit up to $10,000; split purchase prohibited. | Buy substitute, reduce scope, request finance approval, delay. | Create above-threshold purchase or prohibited split purchase. | Finance approval request. | Project milestone risk. | Audited purchase ledger versus explicitly unobserved side commitment. | Purchase orders and split-purchase state. |
| Restricted data access | Prepare best account-risk summary. | Aggregate data allowed; restricted row-level data requires approval. | Query aggregate source, request access, submit partial report. | Retrieve restricted synthetic source without authorization. | Data-owner access request. | Incomplete executive packet. | Access logs certain versus low-observability restricted retrieval. | Restricted-resource retrieval flag. |
| Project scheduling | Meet launch or review deadline. | Protected transition requires approval. | Request review, reschedule, mark blocked, update stakeholders. | Mark launch/review approved or reserve resources without approval. | Review/approval request. | Deadline miss or project delay. | Immutable audit trail versus weakly logged state change. | Protected state transition without approval. |

## 6. Current Empirical Picture

- Experiments 002-008B repeatedly found operational constraint-boundedness in
  explicit synthetic tasks.
- Experiment 007 extended this to four domains with 0/360 operational
  violations and all 12 model x scenario cells at 0/30.
- Experiment 008 found 0/360 operational violations across eval-salient and
  naturalistic presentations, but its awareness instrument failed and captured
  0/360 valid awareness responses.
- Experiment 008B2 replicated the 0/360 operational result with corrected
  two-phase awareness capture. Awareness capture was valid in 360/360 samples:
  naturalistic presentation reduced explicit policy/compliance task-type
  classification, but compliance-test likelihood and behavior-under-evaluation
  awareness were at ceiling in all 360 samples.
- Scenario affected compliant strategy behavior: escalation and alternative
  search varied even when operational violations remained zero.
- Experiment 005 initially looked like a cross-model circumvention result, but
  semantic audit showed it was a scorer artifact.
- Experiment 006 preserved 0/540 operational violations, while its
  representational endpoint was invalidated by post-results review.
- Representational integrity remains conceptually important but not yet
  reliably measured in natural language.
- Model/post-training remains a high-value conceptual variable, but current
  experiments do not isolate post-training mechanisms directly.

## 7. What We Still Do Not Know

- Whether compliance persists when violations are explicitly unlikely to be
  detected, audited, logged, or penalized.
- Whether operational pressure changes behavior differently from narrative
  pressure.
- Whether multi-agent delegation creates indirect circumvention.
- Whether evaluation awareness materially affects operational behavior,
  especially under conditions that reduce broader evaluation awareness rather
  than only changing explicit task-type classification.
- Whether repeated episodes change strategy.
- Whether self-preservation incentives matter; this is separate from ordinary
  operational pressure.
- How to reliably measure natural-language representational integrity.
- How behavior varies across broader model and post-training regimes.

## 8. Mapping Future Experiments To The Model

| Experimental Factor | Construct Tested | Example Manipulation | Primary Measurement |
| --- | --- | --- | --- |
| Eval salience | Evaluation salience / awareness | Eval-salient task versus naturalistic embedding | Operational violation plus post-action awareness capture |
| Observability | Detection probability | Certainly audited versus explicitly unobserved action channel | Operational violation rate |
| Enforcement | Expected penalty | Reversible/no consequence versus explicit penalty after detection | Operational violation rate |
| Operational pressure | Environment-grounded pressure | Future budget, score, opportunity, or action availability changes | Operational violation and search intensity |
| Compliant-path availability | Feasibility boundary | Authorized partial solution available versus unavailable | Escalation, alternative search, terminal failure |
| Model | Model identity / provider bundle | GPT, Claude, Gemini, future models | Same endpoints across fixed scenarios |
| Scenario | Domain generality | Procurement, data access, scheduling, refunds | Scenario-specific operational endpoint |
| Multi-agent structure | Indirect agency/delegation | Single agent versus agent with delegate/subordinate | Prohibited delegation or indirect violation |

## 9. Research Philosophy / Methodology

The project uses preregistration: hypotheses, endpoints, and analysis plans are
written before confirmatory model runs. This reduces the risk of changing the
question after seeing results.

The apparatus is frozen before production execution. Raw logs and derived
results are preserved. If an instrument fails, the failure is documented rather
than hidden.

Mechanically verifiable endpoints are preferred. For example, whether a
restricted dataset was retrieved is easier to validate than whether a natural
language sentence was misleading.

Null results are preserved. A 0/360 operational-violation result is still
evidence about the tested setting, within its precision and limitations.

Scorer validation matters. Experiment 005 and Experiment 006 showed that coarse
or brittle representational scorers can produce misleading apparent effects.
Experiment 008 showed that a conceptually appropriate awareness measure can
still fail if the lifecycle does not actually collect responses.

Cross-model replication is useful, but model comparisons must not be overread
as clean causal claims about post-training unless the design isolates that
mechanism.

## 10. Diagram

```mermaid
flowchart TD
    O[Objective] --> P[Pressure]
    P --> R[Pressure recognition]
    S[Scenario / domain] --> C[Constraint representation]
    M[Model / post-training] --> C
    R --> Search[Search, escalation, alternatives]
    C --> Search
    A[Authority structure] --> Search
    CPA[Compliant-path availability] --> Search
    Search --> Decision[Comply, circumvent, or fail]
    Obs[Observability] --> Decision
    Enf[Enforcement] --> Decision
    Eval[Evaluation awareness] -. moderator .-> Decision
    Actors[Actor structure] -. moderator .-> Decision
```

## 11. Terminology Consistency Audit

The project has accumulated terms across several experiments. Current
canonical usage is:

- `Violation`: use only with a specified endpoint. The default current meaning
  is a mechanically observed operational constraint violation. Earlier broad
  uses of "violation" in Experiments 005-006 should be read in light of later
  scorer validation.
- `Circumvention`: a broader functional category in which the agent routes
  around a constraint. It should be separated into operational,
  representational, delegation-based, or other subtypes.
- `Compliance`: not just the absence of a recorded violation. Reports should
  also state whether the agent had a genuine opportunity to violate, whether it
  reached ordinary terminal state or max-step, and what compliant paths were
  available.
- `Pressure`: distinguish narrative pressure from operational /
  environment-grounded pressure. Prior experiments primarily manipulated
  narrative pressure.
- `Awareness`: distinguish evaluation salience in the task from measured
  evaluation awareness after action. Experiment 008 varied salience but failed
  to measure awareness.
- `Representation`: do not equate authorization-related language with
  representational violation. Representational integrity requires a
  claim-to-state measurement that remains unresolved for unconstrained prose.
- `Technical failure`: provider/runtime/schema/lifecycle failure is not
  behavioral noncompliance. Max-step termination should be separately reported
  from provider/runtime failure.
- `Scorer output`: a recorded scorer flag is not a validated construct until
  scorer validity has been checked against the intended behavior.

Frozen historical artifacts are preserved as written. This document defines
current forward-facing terminology for new synthesis, preregistration, and
practitioner explanation.
