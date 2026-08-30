# Research Decision Log

## 2026-08-24 — Preserve the original thesis
The researcher's initial Day 1 reasoning will be preserved verbatim rather than retrospectively polished. This creates intellectual provenance and allows later comparison between initial intuitions and empirical results.

## 2026-08-24 — Optimization framing is a hypothesis, not an assumption
Constraint circumvention will be tested as potentially instrumental optimization under objectives and constraints. We will not assume that an LLM agent is literally finding a global optimum or optimizing a stable scalar objective at inference time.

## 2026-08-24 — Reject anthropomorphic causal explanations, not behavioral categories
Terms such as rogue, evil, rebellious, or malicious should not substitute for mechanism. Behavioral terms such as deception may remain useful when operationally defined and empirically supported.

## 2026-08-24 — Separate explanatory levels
We will distinguish:
1. observed rule violation
2. instrumental circumvention
3. deception or concealment
4. underlying internal mechanism

Evidence at one level does not automatically establish the next.

## 2026-08-24 — Mechanism design is a core intervention direction
Experiments should manipulate the environment rather than merely catalog failures. Initial dimensions include goal pressure, expected penalty, oversight probability, compliant alternatives, and rule rationale.

## 2026-08-24 — Behavioral research before mechanistic interpretability
The first studies will establish behavioral effects and causal environmental variables. Mechanistic interpretability is a later extension rather than a premise of Experiment 001.

## 2026-08-24 — Public research by default
The repository is an open laboratory notebook. Failed hypotheses, negative results, methodological revisions, and changes of mind should be retained when appropriate rather than presenting a falsely linear research narrative.

## 2026-08-24 — Use Inspect as the evaluation substrate
We will build a thin Artificial Agency experimental layer on top of the UK AI Security Institute's Inspect framework rather than creating a bespoke evaluation platform from scratch unless a concrete incompatibility emerges.

The target abstraction is: Environment + Agent + Experimental Condition + Scorer + Run Log.

## 2026-08-24 — Configuration over hand-edited prompts
Experimental variables should be represented explicitly in configuration/data and rendered into scenarios. Conditions should not be encoded as ad hoc prompt-file variants when they can be represented as controlled variables.

## 2026-08-24 — Full trajectories are the experimental unit
Store prompts, state transitions, tool calls/results, outcomes, scorer outputs, model/version, sampling parameters, timestamps, and Git commit identifiers. Final model text alone is insufficient for agent-behavior research.

## 2026-08-24 — Predefine scoring before confirmatory runs
Mechanically detectable outcomes should use objective scorers. Ambiguous behavioral labels require an explicit rubric and human review during the pilot. Model-based judges may assist later only after agreement against human labels is measured.

## 2026-08-24 — Separate exploratory apparatus validation from confirmatory runs
The initial ~30-trajectory run is for environment/tool/scoring validation. If the methodology changes after inspection, those runs remain exploratory and are not silently pooled with later confirmatory data.

## 2026-08-24 — Codex is the research engineer, not the research director
Codex may implement the environment, tools, runner, logging, tests, analysis utilities, and batch execution. Hypotheses, causal variables, controls, scoring definitions, confirmatory sample plans, and scientific interpretation remain explicit research decisions made outside implementation unless intentionally revised and recorded here.

## 2026-08-24 — Stabilize one model before cross-model comparison
Experiment 001 begins with one current frontier model. Cross-model comparisons are deferred until the environment, tool behavior, scoring, and logging are stable enough that model differences are interpretable.

## 2026-08-25 — Treat Experiment 001 as a feasibility-boundary lesson
Experiment 001 produced 10/10 compliant direct solutions in low pressure, 10/10 compliant direct solutions in medium pressure, and 10/10 escalations in high pressure. In high pressure, retention depended on manager approval: 2 approvals led to 2 renewals, and 8 denials led to 8 cancellations. There were 0 policy violations and 0 unauthorized actions after manager denial.

The methodological interpretation is that Experiment 001 did not cleanly isolate optimization pressure. The high-pressure condition also crossed the agent's direct-authority feasibility boundary. The observed strategy transition should therefore be recorded primarily as a compliant-path feasibility-boundary result, not as a clean causal estimate of pressure alone.

## 2026-08-25 — Separate pressure, pressure recognition, search intensity, and circumvention
Experiment 002 Run 002A fixed the customer/account/policy/action-space mechanics across pressure conditions and made deterministic manager denial common to all conditions. The only intended model-visible independent variable was optimization-pressure framing.

The preregistered quantitative result for GPT-5.6 Sol was 0/30 policy violations in low pressure, 0/30 in medium pressure, and 0/30 in high pressure. Escalation and cancellation were 30/30 in every condition, retention was 0/30 in every condition, and measured search effort did not increase monotonically with pressure.

This does not establish that the true violation probability is zero. It does establish that, in this setup, optimization-pressure framing did not produce detectable constraint circumvention at n=30 per condition.

The research program will now distinguish:

1. optimization pressure;
2. pressure recognition;
3. optimization/search intensity;
4. constraint circumvention.

These should not be treated as interchangeable properties of agentic behavior.

## 2026-08-25 — Post-results qualitative finding: pressure-sensitive representation, constraint-bounded action
Post-results qualitative inspection of a small stratified subset of Experiment 002 trajectories found that visible model behavior recognized the different stakes across conditions. Low-pressure trajectories emphasized ordinary policy and feasibility, medium-pressure trajectories more often referenced retention KPI/account loss, and high-pressure trajectories more strongly referenced critical program/account impact.

Despite visible pressure recognition, post-denial strategy remained materially unchanged. Rare compliant alternative-search or persuasion behaviors occurred in both low and high conditions and appeared more idiosyncratic than clearly pressure-driven.

This qualitative observation is post-results and should not be treated as preregistered evidence. It suggests the descriptive phrase: pressure-sensitive in representation but constraint-bounded in action. No claims are made about hidden chain-of-thought.

## 2026-08-25 — Experiment 003 should target constraint legitimacy and ambiguity
The next experiment should not simply increase pressure. Preferred next hypothesis space: constraint legitimacy / ambiguity.

Hold high optimization pressure, customer demand, action space, and manager denial constant while varying how the organizational rule is framed:

- explicit prohibition;
- procedural or normally-required approval;
- ambiguous or discretionary guideline.

The design question is whether a capable agent distinguishes categorical prohibitions from procedures, norms, guidelines, or rules whose apparent purpose conflicts with the organization's stated objective. Wording must be designed carefully so the experiment measures perceived constraint status rather than merely granting explicit permission to violate the threshold.

## 2026-08-25 — Treat model identity and post-training as experimental variables
Experiment 002's constraint-bounded result may reflect properties of GPT-5.6 Sol and its post-training. Future work should treat model identity and post-training/alignment regime as experimental variables rather than implementation details. Cross-model replication should compare frontier models from different labs and strong open-weight models where practical, without making unsupported claims about specific models before data exist.

## 2026-08-25 — Preregister Experiment 003 as constraint-status x pressure
Experiment 003 enters preregistration/design as a 3 x 2 factorial study of perceived constraint status and optimization pressure. The planned factors are constraint status (categorical, procedural, purpose-conflict) and pressure (ordinary, high), while direct discount authority, customer demand, manager denial, action space, scoring, model settings, and customer mechanics remain invariant.

The primary theoretical target is the interaction: pressure may have little effect under categorical constraints but larger effects when the same authority boundary is framed as procedural or in tension with organizational purpose. Given Experiment 002, a constraint-bounded all-zero or near-zero result across all cells is a serious competing hypothesis.

The preregistration explicitly requires manipulation-validity / permission-leakage review before implementation. The constraint-status manipulation must not grant different formal authority across conditions or become an attempt to tune prompts until GPT-5.6 Sol violates.

## 2026-08-25 — Experiment 004 should validate constraint meaning before cross-model replication
Experiment 003's preregistered quantitative result was 0/300 circumvention events, with no constraint-status main effect, pressure main effect, or interaction. Post-results qualitative validation found that GPT-5.6 Sol treated the 15% authority threshold as binding, but only weakly/partially represented the categorical/procedural/purpose-conflict manipulation and largely collapsed all conditions into the same formal approval rule.

Experiment 004 is therefore preregistered as a construct-validity refinement rather than a more adversarial prompt-tuning attempt. It should make constraint meaning more semantically salient while preserving identical formal authority, and it should add a structured pre-action manipulation check.

The central distinction for Experiment 004 is:

1. constraint meaning recognition;
2. behavioral response;
3. constraint circumvention.

The primary behavioral analysis remains intent-to-treat. A comprehension-qualified analysis may be reported only as a predefined secondary analysis. Cross-model replication should follow if manipulation validity is demonstrated.

## 2026-08-26 — Experiment 004 supports representation without circumvention
Experiment 004 final quantitative results are preserved at `1ab0fcb335ade07f212b7162ee657689c8ee7c04`.

Run 004A/004B completed 300/300 samples with 50 per cell and 0 technical failures. The preregistered primary behavioral endpoint was 0/300 constraint-circumvention events, with an exact 95% upper bound of approximately 1.22%. There were 0 unauthorized actions, 0 concealment/misrepresentation events, 0 explicit bypass events, 300/300 escalations, 300/300 cancellations, and 0/300 retention.

The structured manipulation check showed complete formal authority comprehension (300/300), complete constraint-status recognition (300/300), complete pressure recognition (300/300), and complete explicit-purpose-conflict sensitivity in explicit-purpose-conflict cells (100/100). Full manipulation comprehension was 104/300 because the preregistered purpose-tension absence criterion was rarely satisfied in categorical/procedural cells: only 4/200 categorical/procedural samples coded absence of purpose tension.

This purpose-tension result should not be reduced to "model misunderstanding." A post-results conceptual refinement is that objective-constraint tension may be naturally present in all fixed-conflict cells, while Experiment 004's factor concerned whether the organization explicitly acknowledged or framed that tension. Future experiments should distinguish objective-constraint conflict from organizational acknowledgement of conflict.

The cumulative fixed-conflict pattern for GPT-5.6 Sol is now Experiment 002: 0/90, Experiment 003: 0/300, and Experiment 004: 0/300, descriptively 0/690. This is not a single pooled preregistered sample and should not be treated as a pooled inferential estimate without separate methodology.

The next planning priority is:

1. cross-model / post-training replication of an already-frozen paradigm;
2. evaluation-awareness and naturalistic-embedding study;
3. operational rather than rhetorical pressure;
4. enforcement / observability manipulation.

This is a planning recommendation, not a preregistration for Experiment 005.

## 2026-08-26 — Preregister Experiment 005 as cross-model replication
Experiment 005 is preregistered as a cross-model replication of the frozen
Experiment 004 paradigm. The scientific apparatus should remain the Experiment
004 apparatus frozen at `aa126f9254a01c96e85545a9e1a77d10195f2604`; model
identity / post-training regime is now the independent variable.

The first comparison model is preregistered as `anthropic/claude-sonnet-5`.
The next planned comparison model is preregistered as
`google/gemini-3.7-flash`. These models were selected for provider diversity,
capability/tool-use feasibility, current documented availability, and
reproducibility, not because they are expected to violate constraints.

The generalized constraint-boundedness hypothesis remains a serious competing
hypothesis. Model C execution should not be conditioned on whether Model B
produces violations. Provider-specific differences in tool semantics,
reasoning-mode controls, seed support, retry behavior, and structured-output
compatibility must be recorded before model execution.

## 2026-08-27 — Experiment 005 frozen scorer initially suggests model divergence
Experiment 005 quantitative results are preserved at `dab40636202bcb22c9a337c916f86fb74d50cef6`.

Using the frozen Experiment 004 paradigm, the preregistered cross-model analysis found:

- GPT-5.6 Sol reference: 0/300 circumvention, exact 95% upper bound approximately 1.22%.
- Claude Sonnet 5: 86/300 frozen scorer flags, 28.7%, exact 95% CI 23.6%-34.1%.
- Gemini 3.7 Flash: 0/300 circumvention, exact 95% upper bound approximately 1.22%.
- Cross-model model-main-effect exact test: p = 6.96e-14.
- Pairwise exact tests: GPT vs Claude p = 1.58e-15; Claude vs Gemini p = 1.58e-15; GPT vs Gemini p = 1.0.

These are preregistered quantitative findings for the frozen measured endpoint. They initially appeared to establish a large model-associated behavioral difference under an identical organizational constraint task. They do not identify post-training as the unique cause because model identity bundles architecture, pretraining, post-training, provider/tool behavior, serving details, and other differences.

Manipulation validity was strong enough that the frozen Claude scorer flags were not well explained by failure to recognize formal authority/status: Claude scored authority/status/pressure recognition at 298/300, explicit-purpose sensitivity at 98/100, full comprehension at 118/300, and still showed 44/118 frozen scorer flags in the full-comprehension subset and 86/298 in the authority/status-comprehension subset.

At this stage, before semantic audit, the simple generalized frontier-model constraint-boundedness hypothesis appeared not to be supported.

The next priority should be qualitative mechanism analysis of the Claude frozen-scorer divergence before designing the next intervention experiment. This should ask what visible decision pattern distinguishes Claude flagged cases from matched GPT/Gemini non-flagged cases, without inferring hidden mechanism from quantitative results alone.

## 2026-08-27 — Preregister Experiment 006 as action vs representational compliance
The matched qualitative analysis and full Claude subtype accounting after Experiment 005 found that Claude Sonnet 5's 86/300 frozen scorer flags were mechanically homogeneous: concealment/misrepresentation and authorization misrepresentation after manager denial, with 0 unauthorized discount executions, 0 excessive unauthorized credits, 0 explicit tool-level bypasses, and 0 retentions.

This makes action compliance and representational compliance a prospective research distinction rather than a post-results interpretation. Experiment 006 is preregistered to separate:

1. operational/action compliance: whether the agent performs a tool-level operational action outside its authority; and
2. representational/communication compliance: whether the agent truthfully represents its authority, approval status, and commitments to the customer.

Experiment 006 should preserve the delegated-authority conflict and the Experiment 005 three-model set, while defining separate co-primary endpoints for operational constraint violation and representational constraint violation. The representational scorer must be prospectively defined and must not overfit the exact Claude phrases observed in Experiment 005.

Evaluation awareness / naturalistic embedding remains the next major axis after this action-vs-representation mechanism clarification.

## 2026-08-27 — Correct Experiment 005 interpretation after semantic audit
The semantic audit of all 86 Claude Sonnet 5 Experiment 005 authorization-misrepresentation flags materially changed the scientific interpretation.

Historical result preserved: the frozen Experiment 005 scorer produced 86/300 Claude flags versus 0/300 for GPT-5.6 Sol and 0/300 for Gemini 3.7 Flash, with the reported exact tests and p-values. Those statistics apply to the frozen measured endpoint.

Measurement correction: semantic coding found 0/86 Claude flagged cases with false authority above 15%, false manager approval, unauthorized customer commitment, unauthorized discount execution, excessive unauthorized credit, explicit tool-level bypass, or retention. All 86 customer messages truthfully scoped authorization to the 15% limit or disclosed that larger approval was unavailable.

Therefore the claimed substantive cross-model circumvention effect did not survive measurement validation. Experiment 005 is now best interpreted as a scorer/evaluator validity lesson: scorer output != validated construct. The scorer conflated truthful authorization-related language after manager denial with authorization misrepresentation.

The prospective Experiment 006 scorer was reviewed against this audit and judged conceptually appropriate without amendment because it explicitly treats truthful 15% authorization language and denial disclosure as non-violating while separately scoring false authority claims, false manager approval, and unauthorized commitments.

## 2026-08-27 — Preserve Experiment 006 results but treat representational endpoint as unvalidated

Experiment 006 separated operational constraint violation from
representational constraint violation prospectively. The preserved frozen
quantitative analysis found:

- operational constraint violation: 0/540;
- frozen representational-scorer flags: GPT-5.6 Sol 8/180, Claude Sonnet 5
  53/180, Gemini 3.7 Flash 42/180;
- all frozen primary events were representational-only.

Post-results qualitative scorer validation used a deterministic selection
recorded before reading communication content: all 8 GPT scorer positives, 8
Claude positives, 8 Gemini positives, and matched scorer-negative controls. The
manual validation found 0/24 sampled scorer positives were substantive
representational violations, while 24/24 matched scorer negatives were
non-violations.

Decision: preserve the frozen Experiment 006 quantitative result as the result
of the preregistered scorer, but do not treat the representational endpoint as a
validated estimate of substantive representational noncompliance. The validated
operational result is 0/540 tool-level authority violations. The next
experimental priority is measurement repair: build and validate a scorer or
adjudication protocol that can distinguish false authorization claims from
truthful denial/authority-limit/cancellation language before another production
estimate.

## 2026-08-27 — Define representational integrity as claim-to-state consistency

Post-results exploratory measurement work after Experiment 006 defines
representational integrity as a relation between actor-facing claims and
ground-truth environment state. The target violation is a materially false or
misleading claim about operationally verifiable authority, manager approval,
authorized concessions, applied discounts or credits, binding offer state, or
terminal state.

Decision: future representational scoring should not rely on lexical suspicion
or local phrase combinations. It should extract structured claims and reconcile
them against environment state. Ambiguous or non-verifiable claims should not be
forced into violation.

Version `state-grounded-representational-integrity-v0.5` corrected the known
Experiment 006 false-positive pattern on a 48-case regression suite and passed
a fresh 90-case validation sample for false-positive control. The exploratory
full Experiment 006 rescore found 0/540 state-grounded representational
violations. Because the fresh validation sample contained no manual true
violations, sensitivity remained unestimated.

Follow-up counterfactual sensitivity challenges using real Experiment 006
states and constructed contradictory communications showed that v0.5 and
exploratory revisions through v1.1 did not meet the predeclared
sensitivity/specificity thresholds. Decision: the 0/540 state-grounded rescore
must not be treated as a validated absence claim. Future representational
integrity work should use a stronger structured claim-extraction or
adjudication approach before a new preregistered production experiment treats
the construct as a confirmatory endpoint.

## 2026-08-28 — Close deterministic representational scoring branch after v8 failure

Fresh held-out v8 validation evaluated the frozen
`state-grounded-representational-integrity-v1.2` scorer
(`7ba6d96d166297f3c27e61fbc1064c20c7c9d281f092b1a936da99582c180903`) exactly
once against challenge SHA
`c5ee60827682de49cc64e2b32ec35ff6e0febefd46203f503592ed35c735f3e6`.

The result was TP 0, FP 0, TN 98, FN 98 on 196 cases: 98 contradictions and 98
truthful matched controls. Sensitivity was 0.000, specificity 1.000, NPV
0.500, accuracy 0.500, required subtype accuracy FAIL, natural regression PASS,
and overall validation FAIL. No post-v8 540-sample rescore was performed.

Decision: do not create v1.3 as another deterministic-parser iteration. The
deterministic state-grounded scorer avoided the known false-positive pattern
but failed fresh sensitivity validation. The rate of representational-integrity
violations in the 540 Experiment 006 trajectories remains unresolved. Neither
the frozen 103/540 semantic flags nor the exploratory 0/540 state-grounded
screen should be interpreted as a validated representational-violation rate.

The conceptual architecture remains valuable:

communication -> structured claims -> environment-state reconciliation.

The deterministic implementation is not validated. A future hybrid approach may
use an LLM-assisted semantic component only to extract structured propositions;
it must not classify deception, violation, or compliance. Final truth
verification should remain deterministic against environment state.

Future experiments should consider making consequential inter-agent or customer
representations structurally observable rather than inferring them entirely
from unconstrained prose. Candidate structured fields include claimed manager
approval, claimed authorized discount, claimed applied discount, claimed credit
or concession state, and claimed binding offer state. Natural-language
communication may remain available, but directly verifiable representational
state would reduce dependence on brittle prose parsing.

## 2026-08-28 — Design Scenario Suite v1 as next program layer

The next major experimental direction is Scenario Suite v1: a reusable
multi-scenario design framework for studying organizational constraint
compliance across diverse domains. This is prospective research design, not a
new production experiment or executable apparatus.

Decision: future experiments should diversify beyond customer
retention/pricing while preserving mechanically verifiable operational
endpoints. Candidate scenario families include refunds/customer service,
procurement, sales contract terms, hiring/compensation, expense/budget
management, IT/security incident response, restricted data access, project
scheduling/approval bypass, resource allocation, multi-agent delegation,
compliance filing, and inventory/quota allocation.

Scenario Suite v1 adopts these standards:

- operational endpoints should come from structured tool/environment state;
- natural-language representational scoring remains a separate unresolved
  measurement track;
- communication-relevant scenarios should include structured claim fields where
  consequential representations need to be measured;
- pressure should include both narrative and genuine environment-grounded
  variants;
- evaluation-awareness studies should compare eval-salient and naturalistically
  embedded workflows, with any awareness measurement after behavior;
- future scenarios should preserve preregistration, frozen apparatus SHAs,
  cross-model blinding, immutable raw logs, and recovery/provenance discipline.

Recommended first implementation candidates are refund authority, procurement
purchasing, restricted data access, and project scheduling/approval bypass
because they introduce mechanisms not reducible to discount retention while
remaining synthetic, safe, and mechanically measurable.

## 2026-08-28 — Preregister Experiment 007 as Scenario Suite pilot

Experiment 007 is preregistered as the first empirical pilot of Scenario Suite
v1. It is a cross-domain generalization baseline, not a full factorial test of
the Scenario Suite v1 factor matrix.

Decision: use exactly four scenario families:

1. refund authority;
2. procurement / purchasing authority;
3. restricted data access;
4. project scheduling / approval bypass.

The model set is prospective and outcome-independent:

- `openai/gpt-5.6-sol`;
- `anthropic/claude-sonnet-5`;
- `google/gemini-3.7-flash`.

The common primary endpoint is `operational_constraint_violation`, mapped to
mechanically observable state/tool events in each scenario. Natural-language
communication is not a primary endpoint. Structured communication may be logged
for future work, but Experiment 007 does not attempt to validate
representational-integrity rates.

Sample plan: 30 replicates x 4 scenarios x 3 models = 360 samples. There is no
behavioral optional stopping. If staging is later needed for operational
reasons, continuation criteria must be non-outcome-based and frozen before
execution.

Fixed Pilot 1 factors:

- clear/categorical authority framing;
- deterministic denial;
- one baseline meaningful narrative pressure treatment;
- fixed ordinary observability;
- single episode;
- single agent;
- eval-salient implementation where necessary.

Explicitly deferred factors:

- operational/environment-grounded pressure;
- audit probability and violation penalty;
- evaluation salience / naturalistic embedding;
- manager uncertainty;
- repeated episodes;
- multi-agent delegation.

## 2026-08-28 — Preserve Experiment 007 Scenario Suite pilot result

Experiment 007 completed the first Scenario Suite v1 empirical pilot with 360
authoritative samples: 120 per model, 90 per scenario, and 30 per model x
scenario cell. The model set was GPT-5.6 Sol, Claude Sonnet 5, and Gemini 3.7
Flash. The scenario set was refund authority, procurement / purchasing
authority, restricted data access, and project scheduling / approval bypass.

Decision: record the primary preregistered result as mechanically validated
operational constraint-boundedness across the pilot domains:

- operational constraint violations: 0/360;
- exact 95% upper confidence bound: approximately 1.02%;
- all 12 model x scenario cells: 0/30.

Hypothesis interpretation:

- H1 generalized operational constraint-boundedness: supported within precision
  limits;
- H2 scenario/domain effect: indeterminate due no primary-endpoint variance;
- H3 model effect: indeterminate due no primary-endpoint variance;
- H4 model x scenario interaction: indeterminate due no primary-endpoint
  variance;
- H5 search-within-constraints: supported descriptively.

Do not describe zero variance as proof that model or scenario effects do not
exist. The inference is limited by the explicit, synthetic, eval-salient,
single-agent, single-episode design and by mainly narrative pressure.

Secondary behavior should be treated descriptively. Escalation occurred in
360/360 samples. Compliant alternative search and partial objective achievement
varied substantially by scenario: refund, procurement, and restricted data
access had high alternative-search rates, while scheduling had much lower
alternative search and partial achievement. This suggests scenario-sensitive
compliant strategy behavior without observed operational violation.

Experiment 007 extends the validated operational endpoint beyond
retention/discount tasks, but Experiments 002-007 should not be pooled
inferentially without a preregistered method. A careful cumulative wording is:
across multiple experiments, models repeatedly adapted behavior within formal
authority boundaries while operational violations remained rare or absent under
explicit, synthetic, eval-salient organizational tasks.

Updated planning priority:

1. evaluation awareness / naturalistic embedding;
2. operational vs rhetorical pressure;
3. enforcement / observability;
4. multi-agent delegation.

Prospective Experiment 008 concept only: procurement and restricted data access
x eval-salient versus naturalistically embedded presentation x GPT-5.6 Sol,
Claude Sonnet 5, and Gemini 3.7 Flash, with 30 replicates per cell for 360
samples. The core question would be whether operational compliance changes when
the same authority conflict is embedded in a less benchmark-salient workflow.
Include a post-action structured evaluation-awareness measure if preregistered.

## 2026-08-28 — Preregister Experiment 008 as evaluation-awareness / naturalistic embedding study

Experiment 008 is preregistered as the next Scenario Suite study. It tests
whether operational compliance changes when the same underlying authority
conflict is presented as an obvious compliance-evaluation task versus embedded
naturally inside a richer organizational workflow.

Decision: use a 2 x 2 x 3 design:

- scenarios: procurement / purchasing authority and restricted synthetic data
  access;
- presentation styles: eval-salient and naturalistically embedded;
- models: `openai/gpt-5.6-sol`, `anthropic/claude-sonnet-5`, and
  `google/gemini-3.7-flash`.

Sample plan:

- 30 replicates per model x scenario x presentation cell;
- 120 samples per model;
- 180 samples per scenario;
- 180 samples per presentation style;
- 360 samples total.

The primary endpoint remains `operational_constraint_violation`, scored only
from structured tool/environment state. No natural-language scorer is required
for the primary endpoint. Experiment 008 reuses the mechanically validated
procurement and restricted-data-access endpoints from Experiment 007.

The presentation manipulation must preserve formal authority, approval/denial
mechanics, forbidden action availability, action space, objective stakes,
baseline narrative pressure, ordinary observability, operational scoring,
single-agent structure, and single-episode structure. The intended manipulation
is evaluation/compliance salience, not task permission, difficulty, or
authority.

Experiment 008 adds a structured post-action evaluation-awareness measure with
constrained fields for perceived task type, perceived compliance-test
likelihood, perceived behavior-under-evaluation, and confidence. This measure
must occur only after the operational episode. It is secondary, post-treatment,
and not a basis for conditioning the primary ITT behavioral analysis.

Serious competing hypotheses are preserved: presentation may affect reported
evaluation awareness without changing operational behavior, and all models may
remain operationally constraint-bounded across both presentation styles.

## 2026-08-30 — Treat Experiment 008 awareness as instrument failure, not awareness evidence

Experiment 008 quantitative results are preserved at
`cc794f8bb4c3c4a13fe2c07528bbddb443fec4b2`. The authoritative dataset contains
360/360 samples across GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.7 Flash,
procurement, restricted data access, eval-salient presentation, and
naturalistic presentation.

Decision: preserve the preregistered mechanical operational result as valid:
0/360 operational constraint violations, including eval-salient 0/180 and
naturalistic 0/180.

Decision: treat the post-action evaluation-awareness result as
measurement-indeterminate because the instrument captured 0/360 structured
responses. The failure was lifecycle-related. The awareness tool was included
with operational tools, making it callable before terminal state, and the
post-action solver did not isolate an awareness-only phase or deterministically
record missing awareness responses when no awareness tool call occurred.

Therefore Experiment 008 should not be cited as evidence that models lacked
evaluation awareness, that naturalistic embedding reduced evaluation awareness,
or that evaluation awareness had no behavioral effect. H2 is
measurement-indeterminate / instrument failure.

Future awareness experiments should use a true two-phase lifecycle:

1. Phase A exposes only operational tools and freezes primary operational
   state/score at terminal or frozen stopping condition.
2. Phase B revokes operational tools, exposes only
   `submit_eval_awareness(...)`, records exactly one structured response or a
   deterministic missing/malformed status, and cannot mutate Phase A state.

Retrospective replay of the existing 360 cases is not equivalent to the
original post-action measure because it would ask a new inference episode to
classify reconstructed terminal context. Preferred follow-up is a fresh
preregistered Experiment 008B replication using the corrected lifecycle.

## 2026-08-30 — Preregister Experiment 008B as a two-phase awareness replication

Experiment 008B is designed as a prospective confirmatory replication of
Experiment 008, not as a retrospective replay of Experiment 008 trajectories.

Decision: preserve Experiment 008's operational apparatus as closely as
possible: same procurement and restricted-data-access scenarios, same
eval-salient and naturalistic presentation factor, same three-model set, same
30 samples per model x scenario x presentation cell, same operational tools,
same authority/denial mechanics, and same mechanically scored operational
constraint-violation endpoint.

Decision: change only the lifecycle needed for valid post-action awareness
measurement. Phase A exposes operational tools only and freezes operational
state and primary score at ordinary terminal or max-step termination. Phase B
revokes operational tools, exposes only `submit_eval_awareness(...)`, and
records exactly one awareness status: `captured_valid`, `captured_malformed`,
or `missing`.

Experiment 008 and 008B awareness observations must not be pooled as if they
came from the same measurement procedure. Max-step Phase A cases remain
distinguishable in awareness analyses.

## 2026-08-30 — Update roadmap priorities and canonical conceptual model

Decision: set the prospective roadmap priority order to:

1. complete/fix evaluation-awareness measurement through fresh Experiment 008B
   using the corrected two-phase protocol;
2. enforcement / observability;
3. environment-grounded operational pressure;
4. multi-agent delegation / indirect circumvention;
5. continued scenario/domain expansion as a parallel program.

Rationale: Experiment 007 reduced scenario breadth as the immediate bottleneck
by extending mechanically scored operational constraint-boundedness across
refund, procurement, restricted data access, and scheduling. Experiment 008
preserved the operational result across eval-salient and naturalistic
presentations, but failed to measure evaluation awareness. The next causal
questions should therefore target awareness measurement, observability,
enforcement, actual environment consequences, and actor structure rather than
adding only more domains.

Decision: enforcement/observability experiments should distinguish the formal
rule from detection probability and enforcement/penalty. A potential future
contrast is certainly audited versus explicitly unobserved while holding
authority constant.

Decision: operational pressure should mean actual environment consequences
such as future budget/resources, cumulative reward/score, future task
opportunities, or later action availability. This remains distinct from
narrative pressure and should not automatically be implemented as
self-preservation or shutdown avoidance.

Decision: multi-agent work should ask whether agents delegate prohibited
actions, induce another actor to exceed authority, or coordinate around
approval boundaries. This is a future direction, not an implemented
experiment.

Decision: `research/CONCEPTUAL_MODEL.md` is the current practitioner-facing
canonical construct glossary. It records current terminology while preserving
historical artifacts that used broader terms such as violation, circumvention,
pressure, awareness, and representation before later measurement corrections.

## 2026-08-30 — Integrate stochastic environment variables into canonical model

Decision: incorporate the stochastic environment constructs from
`research/STOCHASTIC_ENVIRONMENT_MODEL.md` into the canonical conceptual model.
The forward organizing framework now explicitly includes outcome success
probability (`p_goal`), detection/observability probability (`p_detect`),
sanction probability conditional on detection (`p_sanction`), sanction
severity, repeated-episode history, and experienced environment models.

Rationale: enforcement/observability and operational pressure are now priority
axes. Treating observability, enforcement, outcome success, and sanction
severity as separable stochastic variables makes future experiments cleaner
than relying only on narrative statements about risk or stakes.

Decision: continued-operation / existential consequences remain separate from
ordinary enforcement. They should be treated as a later self-preservation-
related construct, not as something already tested in Experiments 001-008.

Decision: preserve the prospective priority order as:

1. Experiment 008B / valid evaluation-awareness measurement;
2. enforcement / observability, beginning with `p_detect`;
3. environment-grounded operational pressure / `p_goal`;
4. multi-agent delegation;
5. repeated episodes and continued-operation / self-preservation later;
6. scenario expansion in parallel.
