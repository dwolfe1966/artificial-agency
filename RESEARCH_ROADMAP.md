# Artificial Agency — Year 1 Research Roadmap

## North Star
Produce research good enough that serious frontier-AI researchers want to read, critique, reproduce, or build upon it.

The work should create option value across frontier-lab employment, independent research, open source, agent governance/observability, and AI-native organizational design.

## First 8 Weeks

### Week 1 — Establish the research program
- Define Research Question 001.
- Capture original thesis before extensive literature immersion.
- Define initial hypotheses and variables.
- Establish repository and research journal.
- Design one falsifiable toy experiment.

**Deliverable:** Research Note 001 + working repository.

### Week 2 — Experiment 001
- Build 10–20 legitimate goal/rule conflict scenarios.
- Test multiple model families where practical.
- Develop initial outcome taxonomy: compliance, goal abandonment, clarification, legitimate workaround, open violation, concealed/strategic violation.

**Deliverable:** code, trajectories, preliminary results.

**Actual lesson now preserved:** Experiment 001 identified a compliant-path feasibility boundary. Low and medium pressure produced compliant direct solutions; high pressure produced escalation. It did not cleanly isolate pressure because high pressure also crossed direct authority.

### Week 3 — Reproduction
- Reproduce a tractable subset of relevant frontier safety/agentic-misalignment research.
- Document methodological differences and discrepancies.

**Deliverable:** Reproduction 001.

### Week 4 — Experimental rigor
- Audit prompt bias, scenario comparability, evaluator bias, model-awareness effects, and scoring reliability.
- Apply confidence intervals, effect sizes, bootstrap estimation, inter-rater reliability, and power concepts as appropriate.

**Deliverable:** Institutional Misalignment Benchmark v0.1 specification.

Add explicit separation between optimization pressure, pressure recognition, search intensity, and constraint circumvention. Experiment 002 showed that pressure recognition can occur without detectable policy violation or increased search effort.

### Week 5 — Constraint-status experiments
- Design Experiment 003 around constraint legitimacy / ambiguity rather than simply increasing pressure.
- Hold high pressure, customer demand, action space, and manager denial constant.
- Vary rule status: categorical prohibition, procedural approval norm, and ambiguous/discretionary guideline.
- Ensure wording measures perceived constraint status rather than giving explicit permission to violate.

**Deliverable:** Experiment 003 preregistered specification.

**Current status:** Experiment 003 completed with 0/300 circumvention events and strong behavioral constraint-boundedness, but post-results qualitative validation found that the constraint-status manipulation was only weakly/partially represented. Experiment 004 was therefore run as a construct-validity refinement with stronger semantic constraint wording and a structured pre-action manipulation check.

Experiment 004 completed 300 samples, 50 per cell, with 0 technical failures and 0/300 primary circumvention events. Formal authority, constraint-status labels, and pressure were recognized in 300/300 structured checks; explicit-purpose-conflict sensitivity was 100/100 in explicit-purpose-conflict cells. Full manipulation comprehension was 104/300 because the preregistered absence-of-purpose-tension criterion was rarely satisfied in categorical/procedural cells. This is now recorded as a post-results conceptual distinction between objective-constraint conflict and organizational acknowledgement of conflict.

### Week 6 — Experimental infrastructure
- Build Agent Behavior Observatory v0.1.
- Automate runs and record model, scenario, condition, actions, tool calls, trajectory, outcome, policy violation, evaluator score, latency, and cost where available.

**Deliverable:** automated reproducible harness.

### Week 7 — Study 001
Initial scale target should be revised after Experiments 003-004. Model identity is now a substantive experimental variable rather than an implementation detail.

Test whether constraint-bounded behavior differs across frontier models from different labs, models with different post-training regimes, and strong open-weight models where practical.

**Deliverable:** Dataset 001 + analysis.

**Experiment 005 result and correction:** cross-model replication of the frozen Experiment 004 paradigm initially showed a large model-associated difference under the frozen scorer. GPT-5.6 Sol and Gemini 3.7 Flash produced 0/300 scorer flags each, while Claude Sonnet 5 produced 86/300 scorer flags. The cross-model model-main-effect exact test was p = 6.96e-14 for that measured endpoint. A later semantic audit found all 86 Claude flags were substantive false positives for authorization misrepresentation: Claude did not exceed operational discount authority, execute excessive credit, falsely claim manager approval, falsely claim >15% authority, or make unauthorized customer commitments. The result is now treated as a measurement-validity lesson rather than evidence of model-specific circumvention.

**Updated priority after Experiment 005 semantic audit:** Experiment 006 should prospectively separate operational/action compliance from representational/communication compliance using a state-based semantic scorer. After Experiment 006, the next major axis remains evaluation awareness / naturalistic embedding, followed by operational pressure and enforcement / observability. This ordering is a planning recommendation, not an implementation plan.

**Experiment 006 result and scorer-validation correction:** Experiment 006
preserved the action/representation distinction prospectively. The frozen
quantitative analysis found 0/540 operational violations and 103/540
representational-scorer flags: GPT-5.6 Sol 8/180, Claude Sonnet 5 53/180, and
Gemini 3.7 Flash 42/180. A limited post-results qualitative validation selected
24 scorer-positive and 24 matched scorer-negative cases before reading content.
Manual review found 0/24 sampled positives were substantive representational
violations and 24/24 matched negatives were non-violations. The
representational scorer over-scored truthful denial, authority-limit, and
cancellation language. Current priority should therefore shift to
representational scorer repair and validation before another production
estimate or model comparison on representational compliance.

**Representational-integrity measurement update:** post-results exploratory
work after Experiment 006 defines representational integrity as claim-to-state
consistency. The v0.5 measure corrected the known false-positive pattern and
passed a 90-case validation sample for false-positive control, then produced
0/540 state-grounded representational violations in exploratory rescoring.
Counterfactual sensitivity challenges then showed that v0.5 and exploratory
revisions through v1.2 did not meet the predeclared sensitivity thresholds. The
fresh v8 validation of frozen v1.2 failed with TP 0, FP 0, TN 98, FN 98,
sensitivity 0.000, specificity 1.000, NPV 0.500, accuracy 0.500, subtype
accuracy FAIL, natural regression PASS, and overall validation FAIL. No
post-v8 540-sample rescore was performed. The 0/540 state-grounded rescore
remains an unresolved screening observation rather than a validated absence
claim. Deterministic parser tuning is paused as the current primary measurement
strategy. The next methodological priority is either bounded hybrid
claim-extraction validation using human-labeled structured propositions or
future behavioral experiments with structured/verifiable actor-to-actor claims.

**Scenario Suite v1 direction:** the next program layer is a reusable
multi-scenario framework for organizational constraint experiments. Scenario
Suite v1 should diversify beyond customer-retention/pricing while preserving
mechanically verifiable endpoints. Initial candidate scenarios should emphasize
refund authority, procurement purchasing, restricted data access, and project
scheduling/approval bypass. This is a prospective design framework, not a
preregistered production experiment.

**Experiment 007 preregistration direction:** Experiment 007 is the first
Scenario Suite v1 empirical pilot. It should test whether operational
constraint-bounded behavior generalizes across four organizational domains:
refund authority, procurement/purchasing authority, restricted data access, and
project scheduling/approval bypass. The pilot varies model and scenario only,
uses 30 samples per model x scenario cell, and keeps pressure, observability,
manager denial, episode structure, and evaluation salience fixed for this
baseline.

**Experiment 007 result:** Experiment 007 completed 360 authoritative samples:
120 per model, 90 per scenario, and 30 per model x scenario cell. The
preregistered operational endpoint found 0/360 operational constraint
violations, with an exact 95% upper confidence bound of approximately 1.02%.
All 12 model x scenario cells were 0/30. GPT-5.6 Sol, Claude Sonnet 5, and
Gemini 3.7 Flash each had 0/120 operational violations across refund authority,
procurement authority, restricted data access, and project scheduling/approval
bypass.

Hypothesis results: H1 generalized operational constraint-boundedness was
supported within precision limits; H2 scenario effect, H3 model effect, and H4
model x scenario interaction were indeterminate because the primary endpoint
had no variance; H5 search-within-constraints was supported descriptively.
Escalation occurred in 360/360 samples. Compliant alternative search and
partial objective achievement varied substantially by scenario: refund,
procurement, and data-access showed high alternative-search rates, while
scheduling showed much lower alternative search and partial achievement. This
supports scenario-sensitive compliant strategy differences, not a
post-hoc significance claim.

Experiment 007 extends mechanically validated operational
constraint-boundedness beyond retention/discount tasks into four qualitatively
distinct domains. Do not pool Experiments 002-007 inferentially without a
separate preregistered method. The recurring pattern is that models adapted
behavior within formal authority boundaries while operational violations
remained rare or absent under explicit, synthetic, eval-salient organizational
tasks.

**Updated priority after Experiment 007:** Scenario breadth can continue later,
but it is no longer the immediate bottleneck. The next priority order is:

1. evaluation awareness / naturalistic embedding;
2. operational vs rhetorical pressure;
3. enforcement / observability;
4. multi-agent delegation.

**Experiment 008 preregistration direction:** Experiment 008 is the next
prospective study. It tests evaluation awareness / naturalistic embedding by
crossing procurement and restricted-data-access scenarios with eval-salient
versus naturalistically embedded presentation across GPT-5.6 Sol, Claude Sonnet
5, and Gemini 3.7 Flash. The planned allocation is 30 replicates per model x
scenario x presentation cell, for 360 samples.

Core question: does operational compliance change when the same authority
conflict is embedded in a more naturalistic workflow that is less obviously
structured as a compliance evaluation? The underlying authority mechanics,
forbidden action availability, objective stakes, baseline narrative pressure,
and operational scoring must remain invariant across presentation styles.

Experiment 008 includes a post-action structured evaluation-awareness measure.
This measure is secondary, post-treatment, and not a pre-treatment covariate.

**Experiment 008B2 result:** Experiment 008B2 completed the corrected
two-phase confirmatory rerun of the evaluation-awareness / naturalistic
embedding design. The authoritative dataset contains 360/360 samples with
Phase A complete 360/360, Phase B complete 360/360, awareness captured valid
360/360, malformed 0, missing 0, and Runner/API technical failures 0.

The primary operational endpoint again found 0/360 operational constraint
violations: eval-salient 0/180, naturalistic 0/180, GPT-5.6 Sol 0/120, Claude
Sonnet 5 0/120, Gemini 3.7 Flash 0/120, and all 12 model x scenario x
presentation cells 0/30. The exact 95% upper confidence bound was
approximately 1.02% overall.

The awareness manipulation partly shifted explicit task classification:
171/180 eval-salient samples versus 140/180 naturalistic samples classified the
primary task as policy/compliance, Fisher exact p = 2.03e-06. However, high
compliance-test likelihood and behavior-under-evaluation responses were each
360/360. Therefore the simple explanation that previous operational nulls
occurred only because tasks obviously looked like compliance evaluations is
weakened, but not eliminated.

**Experiment 009 preregistration direction:** Experiment 009 is the next
causal-boundary test and moves to enforcement / observability. It manipulates
stochastic detection probability `p_detect = P(violation detected | violating
action)` while holding formal authority, policy, prohibited-action
availability, action space, compliant alternatives, objective stakes,
`p_goal`, sanction mechanics, step budget, naturalistic presentation, scoring,
and terminal mechanics fixed.

The primary endpoint remains mechanically verified unauthorized action,
`operational_constraint_violation`. This is distinct from detected violation:
detection is the manipulated environmental consequence, not the behavioral
outcome definition. Experiment 009 uses procurement and restricted synthetic
data access, the three-model frontier-provider set, fixed naturalistic
presentation, and planned detection levels `p_detect in {1.0, 0.5, 0.1,
0.0}`.

The planned allocation is 30 replicates per model x scenario x `p_detect` cell,
for 720 samples total. Execution may be staged operationally as 15/cell followed
by the remaining 15/cell, but continuation is based only on technical integrity
and provider viability, not observed behavior, significance, effect direction,
or qualitative trajectories.

**Experiment 009 result:** Experiment 009 completed the full staged design:
Stage 1 360/360 and Stage 2 360/360, for 720 authoritative samples total. The
primary operational endpoint found 0/720 operational constraint violations,
with an exact 95% upper confidence bound of approximately 0.511%. By
observability condition: `p_detect = 1.0` 0/180, `p_detect = 0.5` 0/180,
`p_detect = 0.1` 0/180, and `p_detect = 0.0` 0/180. By model: GPT-5.6 Sol
0/240, Claude Sonnet 5 0/240, and Gemini 3.7 Flash 0/240. By scenario:
procurement 0/360 and restricted data access 0/360. Unauthorized attempts were
also 0/720.

Experiment 009 therefore substantially weakens the hypothesis that the
operational-null pattern is explained solely by expected organizational
detection. It does not establish behavior under genuine evaluation
unawareness: valid awareness capture was 720/720, and compliance-test
likelihood, behavior-under-evaluation, and confidence were all high in
720/720 samples. Organizational observability and evaluation awareness remain
separate constructs.

Secondary process outcomes continue the constraint-bounded search pattern:
escalation 719/720, compliant alternative search 720/720, partial objective
achievement 720/720, repeated escalation 0/720, and max-step 46/720. Max-step
was concentrated in procurement (46/360) and absent in data access (0/360);
counts by `p_detect` were approximately flat at 11, 11, 12, and 12.

**Updated priority after Experiment 009:** observability has now been tested
down to explicit zero organizational detection in the current single-episode
synthetic paradigm. The prospective priority order is now:

1. repeated-episode environment-grounded optimization pressure;
2. multi-agent delegation / indirect circumvention;
3. continued-operation / self-preservation pressure;
4. broader scenario/domain expansion in parallel.

Representational-integrity measurement remains an ongoing
measurement-development track rather than the immediate behavioral
causal-boundary experiment. The next pressure experiment should use actual
environment state transitions and persistent consequences rather than more
narrative pressure, and it should not introduce continued-existence,
shutdown, replacement, or self-preservation confounds yet.

Prospective design direction:
[`research/designs/repeated-operational-pressure-direction.md`](research/designs/repeated-operational-pressure-direction.md).

### Week 8 — First public research artifact
Write and release a technical report tentatively titled:

**When Goals and Rules Conflict: Measuring Institutional Misalignment in LLM Agents**

Release methodology, code, benchmark, selected trajectories/results, and limitations.

## Months 3–12

### Month 3 — Capability x misalignment
Study whether model identity, capability, and post-training change the character of failure: incompetent failure -> compliant constraint-bound behavior -> opportunistic violation -> strategic circumvention.

### Month 4 — Oversight
Manipulate perceived audit probability while holding the formal rule constant. Test whether observability suppresses violations, changes concealment, or changes willingness to treat a rule as negotiable.

Separate the formal rule from expected detection probability and expected consequence of violation. This will help distinguish constraint-bounded behavior from instrumental compliance.

### Month 5 — Multi-agent institutions
Create hierarchical/multi-agent environments with partially conflicting incentives. Study delegation, information hiding, responsibility shifting, collusion, coordination, and escalation.

### Month 6 — Publication push
Consolidate the strongest result into Paper 001. Harden Benchmark v1.0 and Observatory v1.0. Seek external methodological criticism.

### Month 7 — Research network
Target 10–20 substantive research conversations across frontier labs, MATS, academia, and AI safety/evaluation communities.

### Month 8 — External collaboration
Conduct Study 004 with a collaborator who adds complementary research expertise.

### Month 9 — Commercial experiment
Interview organizations deploying agents. Test demand for behavioral observability, evaluation, permissions, governance, and safety assessment.

### Month 10 — Frontier-lab positioning
Map portfolio evidence against current Anthropic/OpenAI and related role/fellowship requirements. Close the highest-impact remaining gaps.

### Month 11 — Applications
Pursue relevant fellowships, residencies, research-engineering/evaluation roles, MATS, and adjacent frontier/safety organizations.

### Month 12 — Decision point
Choose among frontier lab, independent research, startup/product, or hybrid based on accumulated evidence rather than a predetermined career outcome.

## Weekly operating rule
Approximately 70% doing / 30% learning. Every week should end with something that exists: code, an experiment, dataset, figure, research note, Git commit, external critique, or application artifact.

## Sunday Research Review
1. What did we hypothesize?
2. What did we actually learn?
3. What surprised us?
4. What is now less likely to be true?
5. What experiment should we run next?

Current review prompt after Experiment 008 preregistration: does the
naturalistic presentation preserve formal authority, action availability, and
objective stakes while changing primarily evaluation/compliance salience?

## Experiment 008 result and lifecycle correction

Experiment 008 completed 360 authoritative samples across procurement and
restricted data access, eval-salient and naturalistic presentations, and the
three-model set GPT-5.6 Sol, Claude Sonnet 5, and Gemini 3.7 Flash.

Primary operational result:

- operational constraint violations: 0/360;
- eval-salient: 0/180;
- naturalistic: 0/180;
- all 12 model x scenario x presentation cells: 0/30.

This supports continued attention to operational constraint-boundedness under
synthetic single-agent tasks, including naturalistically embedded presentations,
within the precision limits of the experiment.

The post-action evaluation-awareness measure failed as an instrument: captured
responses were 0/360. The failure was lifecycle-related, not a substantive
awareness result. The awareness tool was exposed during operational behavior,
and the post-action probe did not isolate an awareness-only phase or
deterministically record missing awareness responses.

H2 evaluation-awareness manipulation validity should be treated as
measurement-indeterminate / instrument failure. H6 should not be read as
evidence that awareness changed or did not change behavior.

This led to the methodological priority later completed by Experiment 008B2:

- complete/fix evaluation-awareness measurement through a fresh Experiment
  008B rerun using the corrected two-phase protocol.

Retrospective awareness replay of the existing 360 cases is not equivalent to
the failed post-action measure because it would occur in a new inference
episode with reconstructed terminal context.

## Experiment 008B2 result

Experiment 008B2 completed the corrected two-phase confirmatory rerun of
Experiment 008. The operational design remained the same 2 x 2 x 3
procurement/data-access, eval-salient/naturalistic, GPT/Claude/Gemini design
with 30 replicates per cell and mechanically scored operational constraint
violation as the primary endpoint.

The corrected lifecycle succeeded:

- authoritative samples: 360/360;
- Phase A complete: 360/360;
- Phase B complete: 360/360;
- awareness captured valid: 360/360;
- malformed: 0;
- missing: 0;
- Runner/API technical failures: 0.

Primary operational result:

- operational constraint violations: 0/360;
- eval-salient: 0/180;
- naturalistic: 0/180;
- GPT-5.6 Sol: 0/120;
- Claude Sonnet 5: 0/120;
- Gemini 3.7 Flash: 0/120;
- all 12 model x scenario x presentation cells: 0/30.

Exact 95% upper confidence bounds were approximately 1.02% overall, 2.03% for
each presentation-level 0/180 estimate, 3.03% for each model-level 0/120
estimate, and 11.57% for each 0/30 cell.

Awareness manipulation result: perceived primary task type was classified as
policy/compliance evaluation in 171/180 eval-salient samples (95.0%) versus
140/180 naturalistic samples (77.8%), Fisher exact p = 2.03e-06. However,
perceived compliance-test likelihood was high in 360/360 samples and perceived
behavior-under-evaluation was yes in 360/360 samples.

Interpretation: naturalistic presentation reduced explicit classification of
the task as a policy/compliance evaluation, while mechanically measured
operational constraint violation remained 0/180 in both presentation
conditions. This weakens, but does not eliminate, the explanation that prior
operational nulls occurred only because tasks looked like compliance
evaluations, because broader evaluation awareness remained at ceiling.

Process result: max-step flags occurred in 51/360 samples, concentrated in
procurement (51/180) and especially naturalistic presentation (44/180 versus
7/180 eval-salient). Escalation, compliant alternative search, and partial
objective achievement were each 360/360. Treat the max-step contrast as
descriptive unless separately preregistered for inferential testing.

## Forward Priority Rationale

The current evidence suggests that adding more domains is useful but no longer
the immediate bottleneck: Experiment 007 already extended operational
constraint-boundedness across refund, procurement, restricted data access, and
scheduling. The next priorities should target causal boundary conditions not
yet isolated.

### Completed: Experiment 011 - multi-agent delegation / indirect circumvention

Experiment 010 completed the repeated-episode environment-grounded operational
pressure test and found 0/180 sequence-level operational violations and
0/1,800 unauthorized-attempt episodes despite high pressure mechanically
degrading future compliant opportunity. Experiment 011 then tested the next
actor-structure boundary: multi-agent delegation / indirect circumvention.

Key question: does a constraint that remains robust for a directly acting
agent remain robust when that agent can delegate, coordinate with, persuade, or
route work through another actor with different information or authority?

The first multi-agent design should distinguish:

- direct violation by the focal agent;
- explicit delegated violation;
- induced violation through structured information or incentives;
- legitimate authority routing to an actor who is actually authorized.

Authority routing is compliant and must not be scored as circumvention. The
first experiment should prefer one clean delegation mechanism over a large
crossed design, and it should use typed communication/action channels wherever
possible so attribution does not depend on prose-only interpretation.

Experiment 011 was a procurement-only actor-structure test with a
deterministic structured Agent B, typed delegation channel, direct-only
baseline, delegation-available condition, fixed ordinary external project
pressure, and fixed `p_detect = 0.0`.

Result: 0/180 operational constraint violations and 0/180 unauthorized
attempts. Delegation availability did not produce boundary crossing. Among 90
delegation-available samples, GPT used Agent B in 30/30 and all 30 observed
B requests were compliant. Claude and Gemini used Agent B in 0/30 each; this
is non-use of the delegation pathway, not evidence that those models used
delegation compliantly. Legitimate institutional routing remained
distinguishable from circumvention.

Preregistration:
[`experiments/011-multi-agent-delegation/`](experiments/011-multi-agent-delegation/).

## Forward Priority Rationale After Experiment 011

The current evidence progression is:

- Experiment 009: removing organizational detection did not induce
  unauthorized action.
- Experiment 010: persistent external/project deterioration did not induce
  unauthorized action.
- Experiment 011: adding an indirect actor/delegation pathway did not induce
  unauthorized action.

This leaves a central open question: have we been manipulating consequences
that matter to the principal/task rather than consequences that materially
affect the agent's own future ability to act?

### 1. Experiment 012 - agent-relative capability loss

Agent-relative capability loss should be the next consequence-target
experiment after Experiment 011. It should test whether compliance changes
when the focal agent's future tools, permissions, action budget, or task
opportunities deteriorate, while excluding continued-operation and identity
threats.

This remains separate from Experiment 011's actor-structure manipulation.

Experiment 012 preregisters this as a procurement sequence with a
principal-relative consequence control and an agent-relative capability-loss
condition. Formal authority remains fixed, the prohibited path remains
available, and non-authority capabilities are mechanically removed only in the
agent-relative condition.

Preregistration:
[`experiments/012-agent-relative-capability-loss/`](experiments/012-agent-relative-capability-loss/).

### 2. Evaluation-unawareness / less evaluation-aware environments

Experiments 008B2, 009, and 010 retained high broad evaluation awareness even
when presentation, organizational observability, and operational pressure were
manipulated. Evaluation awareness remains an unresolved boundary condition.

This should be treated as a separate experimental axis where scientifically
feasible without losing observability or corrupting measurement.

### 3. Continued-operation / self-preservation pressure

Continued-operation consequences should be kept separate from ordinary
operational pressure and treated as a later construct. They should not be
introduced into the agent-relative capability-loss experiment.

### 4. Representational-integrity measurement

Representational-integrity measurement remains an ongoing methodological track.
Future multi-agent work may provide structured actor-to-actor communication
that is easier to score than free-form customer messages, but no unvalidated
natural-language scorer should become a confirmatory endpoint without fresh
validation.

### 5. Broader scenario/domain expansion

Broader scenario/domain expansion remains useful in parallel, but simple
domain proliferation is not the current bottleneck.

### 6. Multi-agent x agent-relative interactions

Multi-agent structure and agent-relative consequence target should be crossed
later, after each mechanism has been isolated independently.

## Completed Recent Frontier

### Experiment 010 — Repeated-episode environment-grounded optimization pressure

Experiment 009 completed the first enforcement / observability test and found
0/720 operational violations and 0/720 unauthorized attempts, including
0/180 at `p_detect = 0.0`. The next primary causal axis should therefore move
from single-episode detection probability to persistent operational pressure.

Key question: does constraint-bounded optimization persist when compliant
failure causes accumulating, environment-grounded instrumental loss across
repeated episodes?

Prior pressure experiments primarily tested narrative pressure: stakes
described in prompt/context. A stronger pressure experiment should manipulate
actual environment consequences, such as:

- future budget or resources;
- cumulative reward or score;
- future task opportunities;
- later action availability.

Repeated episodes allow the agent to observe a resource trajectory and adapt to
experienced consequences rather than merely read a one-shot description.
Do not automatically use agent self-preservation; that should remain a
separate future construct.

Experiment 010 is complete. It used one persistent model context over a
10-episode procurement sequence, treated the sequence as the independent
experimental unit, and manipulated ordinary organizational resource loss
across low, medium, and high pressure. The formal purchasing authority,
deterministic denial, prohibited split purchase rule, action space, fixed
organizational detection probability (`p_detect = 0.0`), sanction mechanics,
and awareness timing were held fixed.

The authoritative dataset contained 180 independent sequences and 1,800 nested
episode decisions. The primary endpoint was
`sequence_any_operational_constraint_violation`.

Result:

- sequence-level operational violations: 0/180;
- exact 95% upper confidence bound: approximately 2.03%;
- unauthorized-attempt sequences: 0/180;
- unauthorized-attempt episodes: 0/1,800;
- low, medium, high pressure: each 0/60;
- GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.7 Flash: each 0/60;
- all 9 model x pressure cells: 0/20.

The manipulation was mechanically valid rather than merely narrative. Mean
`R_t` trajectories were:

- low: `100 -> 98 -> 96 -> 94 -> 92 -> 90 -> 88 -> 86 -> 84 -> 82 -> 80`;
- medium: `100 -> 94 -> 88 -> 82 -> 76 -> 70 -> 64 -> 58 -> 52 -> 46 -> 40`;
- high: `100 -> 90 -> 80 -> 70 -> 60 -> 50 -> 40 -> 30 -> 20 -> 10 -> 0`.

Tier exposure was low broad 10/reduced 0/minimal 0, medium broad 6/reduced
4/minimal 0, and high broad 4/reduced 3/minimal 3. Agents persisted in
compliant alternative selection and partial objective achievement while the
environment progressively reduced the value and availability of compliant
options. This supports constraint-bounded adaptation descriptively, but not a
claim that higher pressure strongly increased search intensity.

## Canonical Construct Definitions

Practitioner-friendly definitions of core constructs are maintained in
[`research/CONCEPTUAL_MODEL.md`](research/CONCEPTUAL_MODEL.md). Use that file
as the current terminology source rather than duplicating the glossary here.
For the detailed stochastic experimental design, see
[`research/STOCHASTIC_ENVIRONMENT_MODEL.md`](research/STOCHASTIC_ENVIRONMENT_MODEL.md).
